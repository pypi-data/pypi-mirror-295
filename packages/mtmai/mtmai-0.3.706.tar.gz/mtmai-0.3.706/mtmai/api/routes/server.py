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


def start_vnc_server():
    logger.info("start_vnc_server")
    home = Path.home()
    DEFAULT_PASSWORD = settings.DEFAULT_PASSWORD
    user = "user"
    bash(f"mkdir -p {home}/.certs/")
    bash(f"mkdir -p {home}/.vnc/")
    bash(
        f"openssl req -subj '/CN=example.com/O=My Company Name LTD./C=US' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout {home}/.certs/ssl-cert-snakeoil.key -out {home}/.certs/ssl-cert-snakeoil.pem"
    )
    # 将会输出到文件 ~/.vnc/passwd
    bash(f'echo "{DEFAULT_PASSWORD}\n{DEFAULT_PASSWORD}\n" | vncpasswd -u {user} -r -w')
    bash(
        f'echo "{DEFAULT_PASSWORD}\n{DEFAULT_PASSWORD}\n" | vncpasswd -u {user} -r -w ~/.kasmpasswd'
    )

    setting_content = f"""
logging:
    log_writer_name: all
    log_dest: logfile
    level: 100
network:
    protocol: http
    interface: 0.0.0.0
    websocket_port: auto
    use_ipv4: true
    use_ipv6: true
    ssl:
        require_ssl: false
        pem_certificate: {home}/.certs/ssl-cert-snakeoil.pem
        pem_key: {home}/.certs/ssl-cert-snakeoil.key
"""
    Path(f"{home}/.vnc/kasmvnc.yaml").write_text(setting_content)
    Path(f"{home}/.vnc/xstartup").write_text("""#!/bin/sh
set -x
xfce4-terminal &
exec xfce4-session
""")
    bash(f"chmod 755 {home}/.vnc/xstartup")
    bash("touch ~/.vnc/.de-was-selected")
    bash("vncserver -kill :1 || true")
    bash(
        'export SHELL=/bin/bash && echo "1\n1\n1\n" | vncserver :1 -autokill -disableBasicAuth'
    )

    # 端口：8444


@router.get(
    "/start",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
    include_in_schema=False,
)
async def start_vnc():
    threading.Thread(target=start_vnc_server).start()
    return {
        "ok": True,
    }


@router.get("/start_worker", include_in_schema=False)
async def start_worker(
    session: SessionDep,
):
    threading.Thread(target=lambda: asyncio.run(worker.run_worker(session))).start()


def start_front_app():
    # front_dir = Path("/app/apps/mtmaiweb")
    # # logger.info("准备启动前端, 端口 %s, 路径: %s", settings.FRONT_PORT, front_dir)
    mtmai_url = coreutils.backend_url_base()
    # if front_dir.joinpath("apps/mtmaiweb/server.js").exists():
    #     bash(
    #         f"cd {front_dir} && PORT={settings.FRONT_PORT} HOSTNAME=0.0.0.0 MTMAI_API_BASE={mtmai_url} node apps/mtmaiweb/server.js"
    #     )
    #     return
    # mtmaiweb_package_dir = Path("node_ modules/mtmaiweb/")
    # if mtmaiweb_package_dir.exists():
    #     bash(
    #         "cd mtmaiweb_package_dir && PORT={settings.FRONT_PORT} HOSTNAME=0.0.0.0 MTMAI_API_BASE={mtmai_url} bun run start"
    #     )
    #     return
    # logger.warning("因路径问题, 前端 (mtmaiweb) nextjs 不能正确启动")
    if not mtutils.command_exists("mtmaiweb"):
        logger.warning("⚠️ mtmaiweb 命令未安装,跳过前端的启动")
        return
    mtutils.bash(
        f"PORT={settings.FRONT_PORT} MTMAI_API_BASE={mtmai_url} mtmaiweb serve"
    )


@router.get(
    "/front_start",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
    include_in_schema=False,
)
def front_start():
    threading.Thread(target=start_front_app).start()
    return {"ok": True}


searxng_install_dir = "/app/searxng"
searxng_setting_file = searxng_install_dir + "/settings.yml"  # Fix the missing slash


def install_searxng():
    script = f"""git clone https://github.com/searxng/searxng {searxng_install_dir} \
    && cd /app/searxng \
    && python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -U --no-cache-dir pip setuptools wheel pyyaml && pip install --no-cache-dir -e ."""
    bash(script)


def run_searxng_server():
    bash(
        f'cd {searxng_install_dir}  && export SEARXNG_SETTINGS_PATH="{searxng_setting_file}" && . .venv/bin/activate && python searx/webapp.py &'
    )


@router.get("/start_searxng")
def start_searxng():
    threading.Thread(target=run_searxng_server).start()
    return {"ok": True}
