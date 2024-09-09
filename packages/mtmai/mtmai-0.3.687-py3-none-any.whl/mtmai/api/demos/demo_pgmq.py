from typing import Any

import psycopg
from fastapi import APIRouter

from mtmai.api.deps import CurrentUser, SessionDep
from mtmai.core.config import settings

router = APIRouter()

# 文档： https://github.com/tembo-io/pgmq/blob/293f6e93f3799ee17016b07f4834f7bd01f7387a/README.md


def execsql(sql: str):
    try:
        # Establishing the connection using context manager
        with psycopg.connect(settings.DATABASE_URL) as connection:  # noqa: SIM117
            with connection.cursor() as cursor:
                cursor.execute(sql)
                datasets = cursor.fetchall()
                return datasets

    except psycopg.Error:
        # Handle database-related errors
        return None


def setup_pgmq():
    """安装必要的插件"""
    return execsql("CREATE EXTENSION IF NOT EXISTS pgmq")


def create_queue(queue_name: str):
    return execsql(f"SELECT pgmq.create('{queue_name}')")


def send_msg(queue_name: str, visible_second: int, count: int):
    return execsql(f"SELECT pgmq.read('{queue_name}', {visible_second}, {count});")


def pop_msg(queue_name: str):
    """Read a message and immediately delete it from the queue. Returns `None` if the queue is empty."""
    return execsql(f"SELECT pgmq.pop('{queue_name}')")


def archive_message(queue_name: str, count: int):
    """Archiving a message removes it from the queue, and inserts it to the archive table."""
    return execsql(f"SELECT pgmq.archive('{queue_name}', {count});")


def read_msg(queue_name: str, msg: str):
    execsql(f"SELECT * from pgmq.send('{queue_name}', '{msg}')")


@router.get("/take")
def take(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    connection = psycopg.connect(settings.DATABASE_URL)
    # Successfully connected to database

    # Creating a cursor
    cursor = connection.cursor()

    # Executing SQL queries
    cursor.execute("SELECT * FROM user")
    datasets = cursor.fetchall()

    for row in datasets:
        print(row)

    # Closing the cursor
    cursor.close()
