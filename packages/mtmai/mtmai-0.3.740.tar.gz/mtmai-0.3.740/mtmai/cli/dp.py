"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliDeploy(Cli):
    """
    一键部署
        含:
        1 构建并发布本项目用到的 npm 包（能公开的部分）
        2 pypi 包, 含本项目及另外几个依赖的包
        3 自动将前端代码部署到 vercel 上，和 cloudflare worker (page) 上
        4 构建主 docker 镜像，并推送到 docker hub 上
        5 自动部署本项目到 huggingface space 上 (含前后端)，以单个 docker 容器方式运行


    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs import dev_helper

        dev_helper.run_deploy()
