import asyncio
import logging
import threading
from dataclasses import dataclass, field

from mtmlib.queue.queue import Message

# from datetime import datetime
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

from mtmai.core.config import settings

logger = logging.getLogger()
# 当消息读取次数大于这个值, 就当作永久失败, 放入死信队列
max_read_count = 10


# @dataclass
# class Message:
#     msg_id: int
#     read_ct: int  # 被读取的次数。
#     enqueued_at: datetime
#     vt: datetime
#     message: dict


@dataclass
class PGMQueue:
    """
    code: https://github.com/tembo-io/pgmq/blob/293f6e93f3799ee17016b07f4834f7bd01f7387a/tembo-pgmq-python/tembo_pgmq_python/queue.py
    """

    DATABASE_URL: str
    delay: int = 0
    vt: int = 30
    pool_size: int = 10
    kwargs: dict = field(default_factory=dict)
    pool: ConnectionPool = field(init=False)

    def __post_init__(self) -> None:  # noqa: D105
        self.pool = ConnectionPool(self.DATABASE_URL, **self.kwargs)

        with self.pool.connection() as conn:
            conn.execute("create extension if not exists pgmq cascade;")

    def create_partitioned_queue(
        self,
        queue: str,
        partition_interval: int = 10000,
        retention_interval: int = 100000,
    ) -> None:
        """Create a new queue

        Note: Partitions are created pg_partman which must be configured in postgresql.conf
            Set `pg_partman_bgw.interval` to set the interval for partition creation and deletion.
            A value of 10 will create new/delete partitions every 10 seconds. This value should be tuned
            according to the volume of messages being sent to the queue.

        Args:
            queue: The name of the queue.
            partition_interval: The number of messages per partition. Defaults to 10,000.
            retention_interval: The number of messages to retain. Messages exceeding this number will be dropped.
                Defaults to 100,000.
        """
        with self.pool.connection() as conn:
            conn.execute(
                "select pgmq.create(%s, %s::text, %s::text);",
                [queue, partition_interval, retention_interval],
            )

    def create_queue(self, queue: str, unlogged: bool = False) -> None:
        """Create a new queue
        Args:
            queue: The name of the queue.
        """
        with self.pool.connection() as conn:
            if unlogged:
                conn.execute("select pgmq.create_unlogged(%s);", [queue])
            else:
                conn.execute("select pgmq.create(%s);", [queue])

    def send(self, queue: str, message: dict, delay: int = 0) -> int:
        """Send a message to a queue"""
        with self.pool.connection() as conn:
            message = conn.execute(
                "select * from pgmq.send(%s, %s,%s);",
                [queue, Jsonb(message), delay],  # type: ignore
            ).fetchall()
        return message[0][0]

    def send_batch(self, queue: str, messages: list[dict], delay: int = 0) -> list[int]:
        """Send a batch of messages to a queue"""
        with self.pool.connection() as conn:
            result = conn.execute(
                "select * from pgmq.send_batch(%s, %s, %s);",
                [queue, [Jsonb(message) for message in messages], delay],  # type: ignore
            ).fetchall()
        return [message[0] for message in result]

    def read(self, queue: str, vt: int | None = None) -> Message | None:
        """Read a message from a queue"""
        with self.pool.connection() as conn:
            rows = conn.execute(
                "select * from pgmq.read(%s, %s, %s);", [queue, vt or self.vt, 1]
            ).fetchall()

        messages = [
            Message(msg_id=x[0], read_ct=x[1], enqueued_at=x[2], vt=x[3], message=x[4])
            for x in rows
        ]
        return messages[0] if len(messages) == 1 else None

    def read_batch(
        self, queue: str, vt: int | None = None, batch_size=1
    ) -> list[Message] | None:
        """Read a batch of messages from a queue"""
        with self.pool.connection() as conn:
            rows = conn.execute(
                "select * from pgmq.read(%s, %s, %s);",
                [queue, vt or self.vt, batch_size],
            ).fetchall()

        return [
            Message(msg_id=x[0], read_ct=x[1], enqueued_at=x[2], vt=x[3], message=x[4])
            for x in rows
        ]

    def pop(self, queue: str) -> Message:
        """Read a message from a queue"""
        with self.pool.connection() as conn:
            rows = conn.execute("select * from pgmq.pop(%s);", [queue]).fetchall()

        messages = [
            Message(msg_id=x[0], read_ct=x[1], enqueued_at=x[2], vt=x[3], message=x[4])
            for x in rows
        ]
        return messages[0]

    def delete(self, queue: str, msg_id: int) -> bool:
        """Delete a message from a queue"""
        with self.pool.connection() as conn:
            row = conn.execute(
                "select pgmq.delete(%s, %s);", [queue, msg_id]
            ).fetchall()

        return row[0][0]

    def archive(self, queue: str, msg_id: int) -> bool:
        """Archive a message from a queue"""
        with self.pool.connection() as conn:
            row = conn.execute(
                "select pgmq.archive(%s, %s);", [queue, msg_id]
            ).fetchall()

        return row[0][0]


# async def consum_messages(*, queue: PGMQueue, queue_name, consumer_fn, vt: int = 10):
#     while True:
#         try:
#             message: Message = queue.read(queue_name, vt=vt)

#             logger.info("拉取到消息 %s", message)
#             if message is None:
#                 await asyncio.sleep(1)
#             else:
#                 consumer_fn(message)
#                 queue.delete(queue_name, message.msg_id)
#         except Exception as e:
#             # TODO: 放入死信队列
#             logger.info("消息消费失败 %s", e)
#             asyncio.sleep(1)


def start_worker_loop():
    logger.info("start_worker_loop")


def get_queue():
    # TODO: 可能需要使用单例, 复用 sql connection
    queue = PGMQueue(settings.DATABASE_URL)
    return queue


@dataclass
class WorkerMain:
    """worker 主入口"""

    queue: PGMQueue | None = None

    # 存储队列名和 处理函数的关系
    handler_dict: dict[str, callable] = field(default_factory=dict)

    def register_consumer(self, *, queue_name, consumer_fn):
        self.handler_dict[queue_name] = consumer_fn

    def run(self):
        threading.Thread(target=self._run_thread).start()

    def _run_thread(self):
        """Run the worker's main logic in an event loop."""
        logger.info("启动worker 主进程")
        asyncio.run(self._start_consumers())

    async def _start_consumers(self):
        """Start all consumers concurrently."""
        tasks = [
            self._consume_messages(queue_name, consumer_fn)
            for queue_name, consumer_fn in self.handler_dict.items()
        ]
        await asyncio.gather(*tasks)

    async def _consume_messages(self, queue_name: str, consumer_fn: callable):
        """Consume messages from a queue and process them using the registered consumer function."""
        while True:
            messages = self.queue.read_batch(queue_name)
            if messages:
                for msg in messages:
                    try:
                        consumer_fn(msg.message)
                        self.queue.delete(queue_name, msg.msg_id)
                    except Exception as e:  # noqa: BLE001
                        logger.info("Message processing failed:  %s", e)
                        if msg.read_ct > max_read_count:  # Failed more than 3 times
                            # TODO: 放入死信队列
                            # dlq.send("dead_letter_queue", msg.message)  # Move to DLQ
                            self.queue.delete(queue_name, msg.msg_id)
                        else:
                            logger.info("Retrying message %s", msg.msg_id)
            await asyncio.sleep(2)
