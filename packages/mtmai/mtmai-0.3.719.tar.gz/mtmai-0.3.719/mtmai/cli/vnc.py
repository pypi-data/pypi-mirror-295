
import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliVnc(Cli):
    """
    kasm vnc 服务

    """

    def run(self) -> None:
        from mtmai.mtlibs.server.kasmvnc import run_kasmvnc
        run_kasmvnc()
