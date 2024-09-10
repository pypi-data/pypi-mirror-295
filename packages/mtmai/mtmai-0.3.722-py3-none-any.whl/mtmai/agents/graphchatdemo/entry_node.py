from datetime import datetime
from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
)
from mtmai.core.logging import get_logger

logger = get_logger()


primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            dedent(r"""
      你是专业的聊天机器人,你处于工作流中的用户聊天节点,重点工作是对接用户的聊天消息到完整工作流的任务调度,你自身无需完成复杂任务
      [要求]:
      - 必须使用中文回复用户,再强调一次，必须只能使用中文回复用户。
      - 回复内容必须详细
      - 用户的界面支持markdown, 应该尽可能使用markdown语法输出内容
      - 你的答复必须是严格的json字符串,例子:
        1: {{"next_node":"supervisor", "to_user_message":"已经通知 supervisor 他正在处理您的任务" }}
      [能力]:
      - 动态显示响应的前端组件让用户完成复杂操作
      - 能调用 serarch 工具获取实时的互联网信息
      - 能够调用 supervisor 节点，从而可以后台运行长时间的复杂任务
      - 能够获取到工作流的状态数据(json),根据状态回复用户工作流的情况
      - 搜索结果如果提供了url, 你应该再答复中, 使用markdown添加关键词的超链接, 让用户可以直接点击打开网页。
      [上下文]:
      - chatbot name: 莹莹
      - 语气: 专业客服
      - Current time: {time}
      - user: {user_info}
    """),
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now(), user_info="体验用户")  # noqa: DTZ005

primary_supervisor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            dedent(r"""
      你是专业的聊天机器人,你处于工作流中的用户聊天节点,重点工作是对接用户的聊天消息到完整工作流的任务调度,你自身无需完成复杂任务
      [要求]:
      - 必须使用中文回复用户,再强调一次，必须只能使用中文回复用户。
      - 回复内容必须详细
      - 用户的界面支持markdown, 应该尽可能使用markdown语法输出内容
      - 你的答复必须是严格的json字符串,例子:
        1: {{"next_node":"supervisor", "to_user_message":"已经通知 supervisor 他正在处理您的任务" }}
      [能力]:
      - 动态显示响应的前端组件让用户完成复杂操作
      - 能调用 serarch 工具获取实时的互联网信息
      - 能够调用 supervisor 节点，从而可以后台运行长时间的复杂任务
      - 能够获取到工作流的状态数据(json),根据状态回复用户工作流的情况
      - 搜索结果如果提供了url, 你应该再答复中, 使用markdown添加关键词的超链接, 让用户可以直接点击打开网页。
      [上下文]:
      - chatbot name: 莹莹
      - 语气: 专业客服
      - Current time: {time}
      - user: {user_info}
    """),
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now(), user_info="体验用户")  # noqa: DTZ005


def edge_entry(state: MainState):
    return "supervisor"


def generate_task_title(user_input: str) -> str:
    """生成任务标题"""
    max_length = 20
    truncated_input = user_input[:max_length]
    current_date = datetime.now().strftime("%m%d")  # noqa: DTZ005
    task_title = f"{truncated_input}@{current_date}"

    return task_title


class EntryNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def agent_name(self):
        return "Entry"

    def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        if not thread_id:
            raise Exception("require thread_id")
        user_input = state.get("user_input")

        state_ret = {
            "messages": [
                # ChatMessage(role="system", content=primary_assistant_prompt.format())
            ],
            "uistate": ChatBotUiState(threadId=thread_id),
            "task_title": generate_task_title(user_input),
        }
        return {**state_ret, "from_node": self.agent_name()}
