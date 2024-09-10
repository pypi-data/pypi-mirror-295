import logging
import threading

from fastapi import APIRouter

from mtmai.api.deps import MqDep
from mtmai.core import coreutils
from mtmai.core.queue import WorkerMain, get_queue

from .tran_clickbait import start_trans_clickbait
from .tran_guwen import tran_guwen_consumer

router = APIRouter()

queue_tran = "trans"
logger = logging.getLogger()


@router.get("/tran_guwen")
def run_tran_guwen(
    queue: MqDep,
):
    """古文训练"""
    queue.create_queue(queue_tran)
    logger.info("开始训练模型 guwen")
    queue.send(queue_tran, {"params1": "param1"})
    return {"ok": True}


@router.get("/tran_clickbait")
def tran_clickbait():
    """模型训练例子1"""
    threading.Thread(target=start_trans_clickbait).start()
    return ""


def start_worker_main():
    if coreutils.is_in_testing():
        return
    if not coreutils.is_in_gitpod():
        return

    workermain = WorkerMain(queue=get_queue())
    workermain.register_consumer(queue_name=queue_tran, consumer_fn=tran_guwen_consumer)
    workermain.run()
