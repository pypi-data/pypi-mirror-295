"""部署相关的子命令"""

import asyncio

from mtmai.cli.cli import Cli
from mtmai.core.logging import get_logger

logger = get_logger()


class CliInit(Cli):
    """
    开发环境项目一键初始化，可在github workspace ,huggingface, gitpod.io 等免费平台一件初始化开发环境。

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs import dev_helper
        from mtmlib.mtutils import is_in_gitpod

        dev_helper.init_project()

        if is_in_gitpod():
            import threading

            from mtmlib import tunnel

            threading.Thread(
                target=lambda: asyncio.run(tunnel.start_cloudflared())
            ).start()

            from mtmai.mtlibs.server.kasmvnc import run_kasmvnc

            threading.Thread(target=run_kasmvnc).start()
