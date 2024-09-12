import logging

from fastapi import APIRouter
from sqlmodel import select

from mtmai.api.deps import CurrentUser, SessionDep
from mtmai.models.models import DocColl, DocCollCreate, DocCollPublic, DocCollsPublic

router = APIRouter()

logger = logging.getLogger()


@router.get("/doccolls", response_model=DocCollsPublic)
async def items(
    db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    statement = (
        select(DocColl)
        .where(DocColl.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    items = db.exec(statement).all()
    return DocCollsPublic(data=items, count=len(items))


@router.post("", response_model=DocCollPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: DocCollCreate
) -> any:
    """
    新建知识库
    """
    item = DocColl.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
