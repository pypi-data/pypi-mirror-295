"""客户端代码生成"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliGen(Cli):
    """openapi 客户端代码生成 含 typescript 和 python"""

    def run(self) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.gen()
