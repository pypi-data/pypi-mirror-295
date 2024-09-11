import asyncio
import logging

logger = logging.getLogger()


# class CliSelenium:
#     """
#     selenium 服务

#     """

#     def run(self, *args, **kwargs) -> None:



def register_selenium_commands(cli):
    @cli.command()
    def selenium():
        from mtmai.mtlibs.server.selenium import start_selenium_server

        asyncio.run(start_selenium_server())