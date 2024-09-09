from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    import mtmai


class AgentTaskBase(SQLModel):
    title: str | None = Field(default="")
    description: str | None = Field(default="")
    path: str | None = Field(default="")
    share_path: str | None = Field(default="")


class AgentTask(AgentTaskBase, table=True):
    """对应 langgraph 一个工作流的运行"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    thread_id: str
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="agenttasks")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    output: str | None = Field(default="")
    config: RunnableConfig = Field(sa_column=Column(JSON))


class AgentMeta(BaseModel):
    id: str
    name: str
    base_url: str
    chat_url: str | None = None
    can_chat: bool = (False,)
    agent_type: str | None = None
    graph_image: str | None = None
    label: str | None = None
    description: str | None = None


class UiMessageBase(SQLModel):
    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True

    thread_id: str = Field(default=None, max_length=255, min_length=10)
    component: str = Field(default=None, max_length=64, min_length=1)  # 可能过时了。
    props: dict = Field(default_factory=dict, sa_column=Column(JSON))  # 可能过时了。
    artifacts: list[dict] = Field(default_factory=list, sa_column=Column(JSON))


class UiMessage(UiMessageBase, table=True):
    """前端 聊天机器人的消息列表组件"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="uimessages")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class UiMessagePublic(UiMessageBase):
    persist: bool | None = True


# ui 状态相关开始
class ChatBotUiStateBase(SQLModel):
    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True

    agent: str | None = None
    layout: str | None = None
    theme: str | None = None
    threadId: str | None = None
    config: dict = Field(default_factory=dict, sa_column=Column(JSON))


class ChatBotUiState(ChatBotUiStateBase):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="uimessages")


class ArtifaceBase(SQLModel):
    artiface_type: str
    title: str | None = None
    description: str | None = None
    # content: str | None = None
    props: dict = Field(default_factory=dict, sa_column=Column(JSON))


class AgentViewType(str, Enum):
    SIDEBAR = "sidebar"  # IDE 右侧聊天样式
    POPUP = "popup"  # 页面中央弹出式


class AgentBootstrap(SQLModel):
    """前端获取 agent 的配置
    前端全局agent 加载器会在所有页面加载时，加载一次，根据返回的配置，初始化agent
    """

    # 前端agent 视图类型
    view_type: AgentViewType | None = Field(default=AgentViewType.SIDEBAR)
    # 是否显示浮动按钮
    is_show_fab: bool = Field(default=True)

    # 其他配置以后再补充
