import asyncio
import logging

logger = logging.getLogger()


def register_mtmflow_commands(cli):
    @cli.command()
    def mtmflow():
        from mtmai.mtlibs.server.mtmflow import run_langflow

        logger.info("启动 mtmflow")
        asyncio.run(run_langflow())
        logger.info("启动 mtmflow 完成")