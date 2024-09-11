import asyncio
import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliSelenium(Cli):
    """
    selenium 服务

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs.server.selenium import start_selenium_server

        asyncio.run(start_selenium_server())
