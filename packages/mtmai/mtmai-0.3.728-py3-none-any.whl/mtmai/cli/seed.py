"""部署相关的子命令"""

import asyncio
import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliSeed(Cli):
    """
    数据库初始化

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.core.seed import init_database

        asyncio.run(init_database())
