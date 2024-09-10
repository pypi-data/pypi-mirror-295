import operator
from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from mtmai.models.agent import ArtifaceBase, ChatBotUiState, UiMessageBase

from .ctx import context

agent_name = "mtmaibot"


class MainState(TypedDict):
    error: str | None = None
    next: str | None = None
    user_input: str | None = None
    user_option: str | None = None
    wait_human: bool | None = False
    # messages: Annotated[Sequence[AnyMessage], operator.add]
    # messages: Annotated[Sequence[AnyMessage], operator.add_messages]
    messages: Annotated[list[AnyMessage], add_messages]

    context: context
    uistate: ChatBotUiState | None = None  # 放弃？
    ui_messages: list[UiMessageBase]  # | None = None
    artifacts: Annotated[list[ArtifaceBase], operator.add]
    from_node: str | None = None
    # code: str | None = None
