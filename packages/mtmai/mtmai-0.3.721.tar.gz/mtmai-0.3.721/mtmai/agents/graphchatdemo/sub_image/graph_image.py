import logging

# from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langgraph.graph import StateGraph
from opentelemetry import trace
from typing_extensions import TypedDict

# from pydantic import BaseModel

logger = logging.getLogger()

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


class StateImage2Text(TypedDict):
    model_name: str | None = None
    user_prompt: str | None = None


def entry_text2image():
    pass


def node_text2image_gen():
    pass


class SubGraphText2Image:
    def __init__(self):
        pass

    @property
    def name(self):
        return "graphchatdemo"

    def build_flow(self):
        # nodes = Nodes()

        wf = StateGraph(StateImage2Text)
        wf.add_node("entry_text2image", entry_text2image)
        wf.add_node("node_text2image_gen", node_text2image_gen)
        wf.set_entry_point("entry_text2image")
        wf.add_edge("entry_text2image", "node_text2image_gen")
        # wf.add_edge("chat", "uidelta_node")
        # wf.add_edge("uidelta_node", "chat")
        # wf.add_conditional_edges(
        #     "chat",
        #     should_continue,
        #     {
        #         "tool_call": "tool_call",
        #         "ask_human": "uidelta_node",
        #         "end": END,
        #     },
        # )
        return wf
