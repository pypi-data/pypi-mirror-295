import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliMtmflow(Cli):
    """
    mtmflow 服务

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs.server.mtmflow import run_langflow

        run_langflow()