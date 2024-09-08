"""客户端代码生成"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliGen(Cli):
    """客户端代码生成"""

    def run(self) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.gen()
