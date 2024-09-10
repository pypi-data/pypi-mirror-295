from contextlib import contextmanager
from typing import Annotated

import httpx
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig
from langgraph.channels.context import Context
from sqlalchemy import Engine
from sqlmodel import Session

from mtmai.core.db import getdb


class AgentContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    httpx_session: httpx.Client
    db: Engine
    session: Session


@contextmanager
def make_agent_context(config: RunnableConfig):
    session = httpx.Client()
    db = getdb()
    try:
        yield AgentContext(httpx_session=session, db=db, session=Session(db))
    finally:
        session.close()


context = Annotated[AgentContext, Context(make_agent_context)]
