"""
SmartScraperMultiGraph Module
"""

import operator
from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from mtmai.models.agent import ArtifaceBase, UiMessageBase

from .ctx import context


class BaseState(TypedDict):
    error: str | None = None
    next: str | None = None
    wait_human: bool | None = False
    messages: Annotated[list[AnyMessage], add_messages]

    context: context
    ui_messages: list[UiMessageBase]  # | None = None
    artifacts: Annotated[list[ArtifaceBase], operator.add]
    from_node: str | None = None  # 放弃?
