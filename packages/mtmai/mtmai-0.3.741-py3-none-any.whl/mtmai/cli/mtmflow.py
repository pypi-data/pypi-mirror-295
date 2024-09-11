import asyncio
import logging

logger = logging.getLogger()


class CliMtmflow:
    """
    mtmflow 服务

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs.server.mtmflow import run_langflow

        logger.info("启动 mtmflow")
        asyncio.run(run_langflow())
        logger.info("启动 mtmflow 完成")
