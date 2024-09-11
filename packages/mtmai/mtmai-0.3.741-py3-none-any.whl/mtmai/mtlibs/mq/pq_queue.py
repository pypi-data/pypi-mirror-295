import logging
from dataclasses import dataclass, field

from psycopg.types.json import Jsonb
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from mtmlib.queue.queue import Message

logger = logging.getLogger()
# 当消息读取次数大于这个值, 就当作永久失败, 放入死信队列
max_read_count = 10


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


class AsyncPGMQueue:
    """
    code: https://github.com/tembo-io/pgmq/blob/293f6e93f3799ee17016b07f4834f7bd01f7387a/tembo-pgmq-python/tembo_pgmq_python/queue.py
    """

    # DATABASE_URL: str

    # kwargs: dict = field(default_factory=dict)
    # pool: AsyncConnectionPool = field(init=False)

    def __init__(self, pool=None) -> None:
        # self.DATABASE_URL = DATABASE_URL
        self.pool = pool
        self.delay = 0
        self.vt = 30
        self.pool_size = 10
        #         delay: int = 0
        # vt: int = 30
        # pool_size: int = 10
        #     connection_kwargs = {
        #         "autocommit": True,
        #         "prepare_threshold": 0,
        #     }
        #     self.pool = AsyncConnectionPool(
        #         self.DATABASE_URL, min_size=20, kwargs=connection_kwargs
        #     )

        # pool = AsyncConnectionPool(
        #     conninfo=DATABASE_URL,
        #     max_size=20,
        #     kwargs=connection_kwargs,
        # )
        logger.info("database connecting ...")
        # await pool.open()
        # with self.pool.connection() as conn:
        #     conn.execute("create extension if not exists pgmq cascade;")

    @classmethod
    async def create(cls, DATABASE_URL: str, **kwargs):
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        pool = AsyncConnectionPool(DATABASE_URL, min_size=20, kwargs=connection_kwargs)

        logger.info("database connecting ...")
        await pool.open()

        async with pool.connection() as conn:
            await conn.execute("create extension if not exists pgmq cascade;")

        return cls(pool)

    async def create_partitioned_queue(
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

    async def create_queue(self, queue: str, unlogged: bool = False) -> None:
        """Create a new queue
        Args:
            queue: The name of the queue.
        """
        async with self.pool.connection() as conn:
            if unlogged:
                await conn.execute("select pgmq.create_unlogged(%s);", [queue])
            else:
                await conn.execute("select pgmq.create(%s);", [queue])

    async def send(self, queue: str, message: dict, delay: int = 0) -> int:
        """Send a message to a queue"""
        with self.pool.connection() as conn:
            message = conn.execute(
                "select * from pgmq.send(%s, %s,%s);",
                [queue, Jsonb(message), delay],  # type: ignore
            ).fetchall()
        return message[0][0]

    async def send_batch(
        self, queue: str, messages: list[dict], delay: int = 0
    ) -> list[int]:
        """Send a batch of messages to a queue"""
        with self.pool.connection() as conn:
            result = conn.execute(
                "select * from pgmq.send_batch(%s, %s, %s);",
                [queue, [Jsonb(message) for message in messages], delay],  # type: ignore
            ).fetchall()
        return [message[0] for message in result]

    async def read(self, queue: str, vt: int | None = None) -> Message | None:
        """Read a message from a queue"""
        async with self.pool.connection() as conn:
            rows = await conn.execute(
                "select * from pgmq.read($1, $2, $3);", queue, vt or self.vt, 1
            )

        messages = [
            Message(msg_id=x[0], read_ct=x[1], enqueued_at=x[2], vt=x[3], message=x[4])
            for x in rows
        ]
        return messages[0] if len(messages) == 1 else None

    async def read_batch(
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

    async def pop(self, queue: str) -> Message:
        """Read a message from a queue"""
        with self.pool.connection() as conn:
            rows = conn.execute("select * from pgmq.pop(%s);", [queue]).fetchall()

        messages = [
            Message(msg_id=x[0], read_ct=x[1], enqueued_at=x[2], vt=x[3], message=x[4])
            for x in rows
        ]
        return messages[0]

    async def delete(self, queue: str, msg_id: int) -> bool:
        """Delete a message from a queue"""
        with self.pool.connection() as conn:
            row = conn.execute(
                "select pgmq.delete(%s, %s);", [queue, msg_id]
            ).fetchall()

        return row[0][0]

    async def archive(self, queue: str, msg_id: int) -> bool:
        """Archive a message from a queue"""
        with self.pool.connection() as conn:
            row = conn.execute(
                "select pgmq.archive(%s, %s);", [queue, msg_id]
            ).fetchall()

        return row[0][0]
