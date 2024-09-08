import asyncio
import logging

from sqlmodel import Session

from mtmai.core.config import settings
from mtmai.core.queue import Message, PGMQueue

logger = logging.getLogger()

queue_name = "ping"


def consum_item(msg: Message):
    logger.info("[consum_item] %s", msg)


async def product(mq: PGMQueue):
    counter = 0
    while True:
        new_msg = {"ping": f"ping {counter}"}
        logger.info("产生消息 %s", new_msg)
        mq.send(queue_name, new_msg)
        counter = counter + 1
        await asyncio.sleep(1)


async def run_worker(session: Session):
    logger.info("🚀 worker start(demo) ...")

    queue = PGMQueue(settings.DATABASE_URL)
    queue.create_queue(queue_name)

    await asyncio.gather(
        product(queue),
        queue.consum_messages(
            queue=queue, queue_name=queue_name, consumer_fn=consum_item
        ),
    )
