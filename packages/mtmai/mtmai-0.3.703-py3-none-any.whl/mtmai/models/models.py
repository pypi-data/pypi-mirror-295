from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from pydantic import EmailStr
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    pass


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=6, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=6, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=6, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    # documents: list["Document"] = Relationship(
    #     back_populates="owner", cascade_delete=True
    # )
    # doccolls: list["DocColl"] = Relationship(
    #     back_populates="owner", cascade_delete=True
    # )
    account: "Account" = Relationship(back_populates="owner", cascade_delete=True)

    # chats: "mtmai.models.chat.ChatInput" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )
    # agenttasks: "mtmai.models.agent.AgentTask" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )
    # uimessages: "mtmai.models.agent.UiMessage" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: str
    # avatar: str | None  # 用户头像地址


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# account ##################################################################################
class AccountBase(SQLModel):
    provider: str
    token: str


class Account(AccountBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    owner_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="account")


# items ####################################################################################
# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: str
    owner_id: str


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ---------------------------------------------------------------------------------------------------------------------


class StatusEnum(str, Enum):
    """工作流状态"""

    NEW = "new"  # New state
    PENDING = "pending"  # Waiting for execution
    RUNNING = "running"
    WAITING_FOR_HUMAN = "waiting_for_human"  # Awaiting human intervention
    CONTINUE_AFTER_CONFIRMATION = (
        "continue_after_confirmation"  # Continue after confirmation
    )
    # START = "start"
    END = "end"
    PAUSE = "pause"


# class AgentReport(SQLModel, table=True):
#     id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
#     agent_name: str = Field(index=True)
#     content: str | None = None
#     created_at: datetime = Field(default_factory=datetime.now, nullable=False)
#     updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

# chat_id: str | None = Field(default=None, foreign_key="chatinput.id")
# chat: ChatInput | None = Relationship(back_populates="messages")
# role: str | None = Field(default="user")


# class Knownledge(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     wid: str = Field(index=True)
#     title: str = Field(index=True)
#     content: str = Field(default=None, index=False)


# class Agent(SQLModel, table=True):
#     id: str = Field(primary_key=True)
#     title: str = Field()
#     type: str = Field(default="default")


# 知识库相关


# Shared properties
class DocumentBase(SQLModel):
    class Config:
        arbitrary_types_allowed = True

    title: str | None = Field(default=None, max_length=255)

    collection: str = Field(default="default", index=True)
    meta: dict | None = Field(default={}, sa_column=Column(JSON))
    content: str | None = Field(default=None, max_length=8196)
    content_type: str | None = Field(default=None, max_length=255)


class Document(DocumentBase, table=True):
    """
    通用的基于 postgres + pgvector 的 rag 文档
    注意: 需要提前运行: CREATE EXTENSION IF NOT EXISTS vector
    参考: https://github.com/pgvector/pgvector-python/tree/master
    """

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    embedding: list[float] = Field(sa_column=Column(Vector(1024)))
    owner_id: str = Field(index=True, nullable=True)
    site_id: str = Field(index=True, nullable=True)
    agent_id: str = Field(index=True, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    is_deleted: bool = Field(default=False, index=True)


class DocumentIndex(SQLModel, table=True):
    """文档索引表，用途 独立的向量数据库，通过相似查询定位Document

    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    embedding: list[float] = Field(sa_column=Column(Vector(1024)))
    document_id: str = Field(index=True)


class DocCollBase(SQLModel):
    title: str = Field(default="default", index=True)


class DocColl(DocCollBase, table=True):
    """
    知识库集
    """

    class Config:
        arbitrary_types_allowed = True

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    # owner_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    # owner: User | None = Relationship(back_populates="doccolls")


# Properties to receive on item creation
class DocCollCreate(DocCollBase):
    pass


class DocCollPublic(SQLModel):
    id: str
    owner_id: str
    title: str


class DocCollsPublic(SQLModel):
    data: list[DocCollPublic]
    count: int
