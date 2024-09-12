from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

from mtmai.agents.graphchatdemo.graph import MtmAgent
from mtmai.core.config import settings
from mtmai.core.logging import get_logger

logger = get_logger(__name__)


# class GraphRunner:
#     def __init__(self, *args):
#         pass


async def get_graph(self, name: str):
    logger.info(f"Running flow {name}")

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    await pool.open()
    checkpointer2 = AsyncPostgresSaver(pool)
    agent_inst = MtmAgent()

    graph = agent_inst.build_flow().compile(
        checkpointer=checkpointer2,
        interrupt_after=["human_node"],
        debug=True,
    )
    return graph
