import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliClean(Cli):
    """
    释放系统磁盘

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.run_clean()
