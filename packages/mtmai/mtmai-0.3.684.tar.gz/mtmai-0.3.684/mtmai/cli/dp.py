"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliDeploy(Cli):
    """部署"""

    def run(self) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.run_deploy()
