"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliInit(Cli):
    """
    开发环境项目一键初始化，可在github workspace ,huggingface, gitpod.io 等免费平台一件初始化开发环境。

    """

    def run(self) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.init_project()
