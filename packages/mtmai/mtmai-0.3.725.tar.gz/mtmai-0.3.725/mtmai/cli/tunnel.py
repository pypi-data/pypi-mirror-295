import logging
import threading

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliTunnel(Cli):
    """
    启动网络隧道,在网络受限的环境中，通过隧道也可以全球访问，也是薅羊毛利器
    TODO: 有空可以添加 tor 和 libp2p 网络的支持
    """

    def run(self, *args, **kwargs) -> None:
        import asyncio

        from mtmlib import tunnel

        threading.Thread(target=lambda: asyncio.run(tunnel.start_cloudflared())).start()
