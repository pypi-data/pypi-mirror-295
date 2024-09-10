from textwrap import dedent
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel

from mtmai.agents.graphchatdemo.state import MainState


def edge_supervisor(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    next_to = state.get("next")
    if next_to:
        return next_to
    return "__end__"


supervisor_prompt = dedent("""
Given the conversation above, who should act next?
Or should we FINISH? Select one of: {options}
""")


class SupervisorNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def agent_name(self):
        return "Supervisor"

    async def __call__(self, state: MainState, config: RunnableConfig):
        members = ["HumanChat", "JokeWriter"]
        options = members

        class RouteResponse(BaseModel):
            next: Literal[*options]

        supervisor_system_prompt = (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers:  {members}. \n"
            " HumanChat 能力:\n直接面向终端用户的聊天agent, 将本程序的内部状态以适合人类理解的语言向用户输出对话, 能调用工具动态显示UI组件."
            " JokeWriter 能力: 幽默段子、笑话写手"
            "Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
        )

        options = [*members]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", supervisor_system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    supervisor_prompt,
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))

        supervisor_chain = prompt | self.runnable.with_structured_output(RouteResponse)
        result = supervisor_chain.invoke(state)
        return {"next": result.next, "from_node": self.agent_name()}
