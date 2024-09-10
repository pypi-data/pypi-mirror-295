from typing import Literal

from mtmai.core.config import settings


def get_langgraph_checkpointer(
    checkpointer_type: Literal["memory", "postgres"] = "memory",
):
    if checkpointer_type == "postgres":
        # return get_postgres_checkpointer()
        # return get_async_postgres_checkpointer()
        return get_async_sqlite_checkpointer()
        # from langgraph.checkpoint.postgres import PostgresSaver

        # from psycopg_pool import ConnectionPool
        # # from .postgres_saver import PostgresSaver

        # pool = ConnectionPool(
        #     conninfo=str(settings.DATABASE_URL),
        #     max_size=20,
        # )
        # connection_kwargs = {
        #     "autocommit": True,
        #     "prepare_threshold": 0,
        # }
        # poll2 = AsyncConnectionPool(
        #     # Example configuration
        #     conninfo=settings.DATABASE_URL,
        #     max_size=20,
        #     kwargs=connection_kwargs,
        # )
        # conn = poll2.connection()

        # checkpointer = PostgresSaver(sync_connection=pool)
        # checkpointer.create_tables(pool)
        # return checkpointer

        # conn = pool.connection()
        # with pool.connection() as conn:
        # checkpointer = PostgresSaver(connection=pool)
        # checkpointer = AsyncPostgresSaver(conn)

        # NOTE: you need to call .setup() the first time you're using your checkpointer
        # checkpointer.setup()
        # return checkpointer

        # graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
        # config = {"configurable": {"thread_id": "1"}}
        # res = graph.invoke({"messages": [("human", "what's the weather in sf")]}, config)
        # checkpoint = checkpointer.get(config)

    # from langgraph.checkpoint.memory import MemorySaver

    # memory = AsyncSqliteSaver.from_conn_string(":memory:")
    from langgraph.checkpoint.memory import MemorySaver

    memory = MemorySaver()
    return memory


def get_async_postgres_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    from psycopg_pool import AsyncConnectionPool

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    poll2 = AsyncConnectionPool(
        # Example configuration
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    # conn = poll2.connection()
    checkpointer = AsyncPostgresSaver(poll2)
    return checkpointer


def get_postgres_checkpointer():
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg_pool import ConnectionPool

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    poll2 = ConnectionPool(
        # Example configuration
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    # conn = poll2.connection()
    checkpointer = PostgresSaver(poll2)

    checkpointer.setup()

    return checkpointer

    # # 当前ide的提示： checkpointer: _GeneratorContextManager[PostgresSaver]
    # checkpointer = PostgresSaver.from_conn_string(settings.DATABASE_URL)
    # checkpointer.setup()
    # return checkpointer


def get_async_sqlite_checkpointer():
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    # from psycopg_pool import AsyncConnectionPool

    # connection_kwargs = {
    #     "autocommit": True,
    #     "prepare_threshold": 0,
    # }
    # poll2 = AsyncConnectionPool(
    #     # Example configuration
    #     conninfo=settings.DATABASE_URL,
    #     max_size=20,
    #     kwargs=connection_kwargs,
    # )
    # conn = poll2.connection()
    checkpointer = AsyncSqliteSaver.from_conn_string(":memory:")
    a = next(checkpointer)
    return a
