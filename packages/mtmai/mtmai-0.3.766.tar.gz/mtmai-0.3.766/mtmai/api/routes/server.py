"""
启动相关后台服务

"""

import asyncio
import logging
import threading
import time
from pathlib import Path

from fastapi import APIRouter, Depends
from opentelemetry import trace

from mtmai.api.deps import SessionDep, get_current_active_superuser
from mtmai.core import coreutils
from mtmai.core.config import settings
from mtmai.mtlibs.server.kasmvnc import run_kasmvnc
from mtmai.mtlibs.server.searxng import run_searxng_server
from mtmai.worker import worker
from mtmlib import mtutils
from mtmlib.mtutils import bash

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()


# 官网： https://coder.com/docs/install
def start_code_server():
    config_file = Path.home().joinpath(".config/code-server/config.yaml")
    if not config_file.exists():
        logger.warning("code-server 配置文件不存在, 跳过启动: %s", config_file)
        return
    # 配置要点：
    # 1: 明确指定 SHELL 路径，否则在一些受限环境，可能没有默认的shell 变量，导致：“The terminal process "/usr/sbin/nologin" terminated with exit code: 1.”
    bash(
        "PORT=8622 PASSWORD=feihuo321 SHELL=/bin/bash code-server --bind-addr=0.0.0.0 &"
    )
    time.sleep(2)
    config_content = config_file.read_text()
    logger.info("codeserver 配置: %s", config_content)


@router.get("/start", include_in_schema=False)
async def start():
    threading.Thread(target=start_code_server).start()


@router.get(
    "/start",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
    include_in_schema=False,
)
async def start_vnc():
    threading.Thread(target=run_kasmvnc).start()
    return {
        "ok": True,
    }


@router.get("/start_worker", include_in_schema=False)
async def start_worker(
    session: SessionDep,
):
    threading.Thread(target=lambda: asyncio.run(worker.run_worker(session))).start()


def start_front_app():
    mtmai_url = coreutils.backend_url_base()
    if not mtutils.command_exists("mtmaiweb"):
        logger.warning("⚠️ mtmaiweb 命令未安装,跳过前端的启动")
        return
    mtutils.bash(
        f"PORT={settings.FRONT_PORT} MTMAI_API_BASE={mtmai_url} mtmaiweb serve"
    )


# @router.get(
#     "/front_start",
#     dependencies=[Depends(get_current_active_superuser)],
#     include_in_schema=False,
# )
# def front_start():
#     threading.Thread(target=start_front_app).start()
#     return {"ok": True}


@router.get("/start_searxng")
def start_searxng():
    threading.Thread(target=run_searxng_server).start()
    return {"ok": True}
