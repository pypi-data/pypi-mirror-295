from datetime import datetime

from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils


class PostTabBase(SQLModel):
    name: str | None = Field(default=None)


class PostTab(PostTabBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)


class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    # content: str | None = Field(default=None)


class Post(PostBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    doc_id: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
