from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.graph.message import AnyMessage
from langgraph.prebuilt import tools_condition

from mtmai.agents.graphchatdemo.state import MainState
from mtmai.core.logging import get_logger
from mtmai.models.agent import UiMessageBase

logger = get_logger()


def edge_human_node(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "HumanChat"
    return "supervisor"


primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{messages}"),
        (
            "system",
            dedent(r"""
      你是专业客服聊天机器人,基于以上对话直接向用户输出回复内容
      [要求]:
      - 必须使用中文回复用户,再强调一次, 必须只能使用中文回复用户
      - 回复内容必须详细
      - Use markdown syntax to output content whenever possible
    """),
        ),
    ]
)


class ShowAdminPanelTool(BaseTool):
    name: str = "ShowAdminPanelTool"
    description: str = (
        r"当用户明确要求显示管理面板、后台面板时,显示管理面板给用户进行下一步的操作"
    )
    response_format: str = "content_and_artifact"

    def _run(self):
        return (
            "Operation successful",
            {
                "artiface_type": "AdminView",
                "title": "管理面板",
                "props": {
                    "title": "管理面板",
                },
            },
        )


class ShowTasksInputPanelTool(BaseTool):
    name: str = "ShowTasksInputPanel"
    description: str = (
        r"有用的工具, 向用户UI 显示任务输入的选择器, 让用户选择需要运行的任务"
    )
    response_format: str = "content_and_artifact"

    def _run(self):
        return (
            "Operation successful",
            {
                "artiface_type": "TaskSelect",
                "title": "任务选择器",
                "props": {
                    "title": "任务选择器",
                },
            },
        )


show_admin_panel_tool = ShowAdminPanelTool()
form_tool = ShowTasksInputPanelTool()
human_node_tools = [
    show_admin_panel_tool,
    form_tool,
]


class HumanNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        messages = state.get("messages")
        from_node = state.get("from_node")
        artifacts = state.get("artifacts")
        if artifacts:
            return {"artifacts": [artifacts[-1]]}

        artifacts_output = []

        system_message = primary_assistant_prompt.format_messages(messages=messages)
        llm = self.runnable.bind_tools([*human_node_tools])
        ai_message = await llm.ainvoke(system_message, config)

        output_msgs = [ai_message]
        if ai_message.tool_calls:
            tool_msg = await acall_tool([ai_message], human_node_tools)
            output_msgs.append(tool_msg)
            if tool_msg.artifact:
                artifacts_output.append(tool_msg.artifact)

        ui_messages = []
        if ai_message.content:
            ui_messages.append(
                UiMessageBase(
                    component="AiCompletion", props={"content": ai_message.content}
                )
            )

        return {
            "artifacts": artifacts_output,
            "messages": output_msgs,
            "ui_messages": ui_messages,
            "uistate": state.get("uistate"),
        }


async def acall_tool(messages: list[AnyMessage], tools: list[any]):
    """
    执行消息列表中最后一个函数调用消息,返回调用结果
    提示: 功能的还需要仔细斟酌
    """
    last_message = messages[-1]
    for x in tools:
        if x.name == last_message.tool_calls[0]["name"]:
            tool_call = last_message.tool_calls[0]
            tool_msg = await x.ainvoke(tool_call)
            return tool_msg
    msg = f"工具调用失败 {tools}"
    raise Exception(msg)  # noqa: TRY002
