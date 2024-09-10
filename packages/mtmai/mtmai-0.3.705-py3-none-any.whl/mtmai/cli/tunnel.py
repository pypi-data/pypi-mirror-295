"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliTunnel(Cli):
    """
    启动网络隧道,在网络受限的环境中，通过隧道也可以全球访问，也是薅羊毛利器
    TODO: 有空可以添加 tor 和 libp2p 网络的支持
    """

    def run(self) -> None:
        from mtmlib import tunnel

        tunnel.start_cloudflared()
