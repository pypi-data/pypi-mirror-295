from typing import Any

from fastapi import APIRouter
from sqlmodel import SQLModel, func, select

from mtmai.api.deps import CurrentUser, SessionDep
from mtmai.models.agent import AgentTask, AgentTaskBase
from mtmai.models.models import (
    Item,
)

router = APIRouter()


class AgentTaskPublic(AgentTaskBase):
    id: str
    # owner_id: str


class AgentTaskResponse(SQLModel):
    data: list[AgentTaskPublic]
    count: int


@router.get("", response_model=AgentTaskResponse)
def items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Item)
        count = session.exec(count_statement).one()
        statement = select(AgentTask).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(AgentTask)
            .where(AgentTask.user_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(AgentTask)
            .where(AgentTask.user_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return AgentTaskResponse(data=items, count=count)
