"""
数据库相关操作
"""

"""部署相关的子命令"""

import asyncio
import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliDb(Cli):
    """
    数据库相关操作

    """

    def run(self, *args, **kwargs) -> None:
        import click

        from mtmai.core.seed import init_database

        @click.group()
        def db_commands():
            pass

        @db_commands.command()
        def seed():
            """Initialize the database with seed data."""
            asyncio.run(init_database())

        @db_commands.command()
        def backup():
            """Backup the database."""
            # TODO: Implement database backup logic
            logger.info("Database backup not implemented yet.")

        if args and args[0] in ["seed", "backup"]:
            db_commands()
        else:
            asyncio.run(init_database())
