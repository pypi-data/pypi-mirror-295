from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    pass


class SiteHost(SQLModel):
    domain: str = Field(default=None, max_length=255)
    is_default: bool = Field(default=False)
    is_https: bool = Field(default=False)
    pass


# Shared properties
class SiteBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    hosts: list[SiteHost] = Field(default=[])
    # email: EmailStr = Field(unique=True, index=True, max_length=255)
    # is_active: bool = True
    # is_superuser: bool = False
    # full_name: str | None = Field(default=None, max_length=255)
    # username: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Site(SiteBase, table=True):
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    # hashed_password: str
    # items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    # documents: list["Document"] = Relationship(
    #     back_populates="owner", cascade_delete=True
    # )
    # doccolls: list["DocColl"] = Relationship(
    #     back_populates="owner", cascade_delete=True
    # )
    # account: "Account" = Relationship(back_populates="owner", cascade_delete=True)

    # chats: "mtmai.models.chat.ChatInput" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )
    # agenttasks: "mtmai.models.agent.AgentTask" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )
    # uimessages: "mtmai.models.agent.UiMessage" = Relationship(
    #     back_populates="user", cascade_delete=True
    # )
