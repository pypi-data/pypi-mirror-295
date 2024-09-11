from mtmai.core.logging import get_logger
from mtmai.core.queue import PGMQueue

logger = get_logger(__name__)


def send_message(mq: PGMQueue, queue: str, message: str):
    mq.send(queue=queue, message=message)
