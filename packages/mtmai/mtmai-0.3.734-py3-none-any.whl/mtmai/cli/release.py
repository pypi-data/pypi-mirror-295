"""部署相关的子命令"""

import logging

from mtmai.cli.cli import Cli
from mtmlib.mtutils import bash, is_in_gitpod

logger = logging.getLogger()


class CliRelease(Cli):
    """
    释放版本:
    1 发布到 pypi
    2 发布到 npm
    3 发布到 docker hub
    4 发布到 huggingface(未实现)
    """

    def run(self, *args, **kwargs) -> None:
        import argparse

        parser = argparse.ArgumentParser(description="Release options")
        parser.add_argument("--options1", help="Option 1 for release")
        args, unknown = parser.parse_known_args()

        if args.options1:
            logger.info(f"Release option 1: {args.options1}")
        from mtmai.mtlibs import dev_helper

        if is_in_gitpod():
            bash("git pull")
            pass
        dev_helper.release_py()
