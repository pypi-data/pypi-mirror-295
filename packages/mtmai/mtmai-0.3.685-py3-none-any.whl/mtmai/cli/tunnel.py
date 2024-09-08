"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliTunnel(Cli):
    """启动网络隧道"""

    def run(self) -> None:
        from mtmlib import tunnel

        tunnel.start_cloudflared()
        # parser = argparse.ArgumentParser(description="Tunnel options")
        # parser.add_argument("--options1", help="Option 1 for tunnel")
        # args, unknown = parser.parse_known_args()

        # if args.options1:
        #     logger.info(f"Tunnel option 1: {args.options1}")
        # from mtmai.mtlibs import dev_helper

        # if is_in_gitpod():
        #     bash("git pull")
        #     pass
        # dev_helper.tunnel()
