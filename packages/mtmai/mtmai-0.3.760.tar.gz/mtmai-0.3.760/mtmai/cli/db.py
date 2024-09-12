"""
数据库相关操作
"""

import asyncio


def register_db_commands(cli):
    @cli.command()
    def db_commands():
        """Database related commands"""
        from mtmai.core.seed import init_database

        asyncio.run(init_database())
