import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliVnc(Cli):
    """
    kasm vnc 服务

    """

    def run(self, *args, **kwargs) -> None:
        from mtmai.mtlibs.server.kasmvnc import run_kasmvnc

        run_kasmvnc()

        try:
            while True:
                # Keep the main process running
                import time

                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt. Shutting down VNC server...")
