"""
SmartScraperMultiGraph Module
"""

from copy import deepcopy
from typing import Annotated, List, Optional

from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from pydantic import BaseModel
from typing_extensions import TypedDict

from mtmai.agents.graphs.base_state import BaseState
from mtmai.agents.nodes.graph_iterator_node import GraphIteratorNode
from mtmai.agents.nodes.merge_answers_node import MergeAnswersNode
from mtmai.llm.llm import get_llm_chatbot_default, get_llm_tooluse_default
from mtmai.models.agent import ArtifaceBase, ChatBotUiState, UiMessageBase

from .abstract_graph import AbstractGraph
from .base_graph import BaseGraph


class MainState(BaseState):
    pass
class SmartScraperMultiGraph(AbstractGraph):
    """
    SmartScraperMultiGraph is a scraping pipeline that scrapes a
    list of URLs and generates answers to a given prompt.
    It only requires a user prompt and a list of URLs.

    Attributes:
        prompt (str): The user prompt to search the internet.
        llm_model (dict): The configuration for the language model.
        embedder_model (dict): The configuration for the embedder model.
        headless (bool): A flag to run the browser in headless mode.
        verbose (bool): A flag to display the execution information.
        model_token (int): The token limit for the language model.

    Args:
        prompt (str): The user prompt to search the internet.
        source (List[str]): The source of the graph.
        config (dict): Configuration parameters for the graph.
        schema (Optional[BaseModel]): The schema for the graph output.

    Example:
        >>> search_graph = MultipleSearchGraph(
        ...     "What is Chioggia famous for?",
        ...     {"llm": {"model": "gpt-3.5-turbo"}}
        ... )
        >>> result = search_graph.run()
    """

    def __init__(self):
        pass


    def create_graph(self):
        llm = get_llm_chatbot_default()
        # toolsllm = get_llm_tooluse_default()
        wf = StateGraph(MainState)
        wf.add_node("graph_iterator", GraphIteratorNode(llm))
        wf.add_node("merge_answers", MergeAnswersNode(llm))
        wf.set_entry_point("graph_iterator")
        wf.add_edge("graph_iterator", "merge_answers")

        return wf
