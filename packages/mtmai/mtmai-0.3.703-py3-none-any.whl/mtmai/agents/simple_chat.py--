import logging

from fastapi import APIRouter
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from mtmlib import dbUtils
from sqlmodel import Session

from mtmai.curd.curd_chat import get_conversation_messages
from mtmai.models.chat import MtmChatMessage
from mtmai.models.models import User
from mtmai.mtlibs import aisdk
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()

router = APIRouter()


class SimpleChatAgent:
    """单个 langchain agent 聊天机器人"""

    def __init__(self):
        pass

    @property
    def name(self):
        return "simplechat"

    async def chat(
        self,
        db: Session,
        conversation_id: str,
        user: User | None = None,
    ):
        tools = []
        llm = lcllm_openai_chat("")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant"),
                MessagesPlaceholder("chat_history", optional=True),
                # ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(
            llm.with_config({"tags": ["agent_llm"]}), tools, prompt
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools).with_config(
            {"run_name": self.name}
        )

        # max_user_messages = 10  # 最大用户消息数，超出自动截断，保留末尾的
        chat_messages = get_conversation_messages(
            db=db, conversation_id=conversation_id, limit=20
        )

        chat_history = [{"role": x.role, "content": x.content} for x in chat_messages]

        with dbUtils.transaction_scope(db):
            async for event in agent_executor.astream_events(
                {
                    "chat_history": chat_history,
                },
                version="v2",
            ):
                kind = event["event"]
                if kind == "on_chain_start":
                    if event["name"] == self.name:
                        logger.info("Starting agent %s", self.name)
                elif kind == "on_chain_end":  # noqa: SIM102
                    if event["name"] == self.name:
                        ai_content = event["data"].get("output")
                        db.add(
                            MtmChatMessage(
                                content=ai_content["output"],
                                chat_id=conversation_id,
                                role="assistant",
                            )
                        )
                        print(f"Done agent: {event['name']} with output: {ai_content}")
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield aisdk.text(content)
                elif kind == "on_tool_start":
                    print(
                        f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
                    )
                elif kind == "on_tool_end":
                    ai_content = event["data"].get("output")
                    print(f"Tool output was: {ai_content}")

            data = {}
            # if not conversation_id:
            data["chatId"] = conversation_id
            yield aisdk.data(
                [
                    {
                        "dataType": "uistate",
                        "data": data,
                    }
                ]
            )

            yield aisdk.finish()
