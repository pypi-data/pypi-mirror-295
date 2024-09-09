import logging

from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.prompts import Prompts
from mtmai.agents.graphchatdemo.state import (
    MainState,
)
from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


# def edge_entry_chat(state: MainState):
#     user_input = state.get("user_input")
#     if len(user_input) > 0:
#         return "chat"
#     return "uidelta"


class Nodes:
    # async def finnal_node(self, state: MainState, config: RunnableConfig):
    #     logger.info("finnal_node, %s", state)

    async def mtmeditor_node(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state.get("user_input")
        user_option = state.get("user_option")
        messages = list(state.get("messages"))

        new_user_message = ChatMessage(role="user", content=user_input)
        messages.append(new_user_message)
        llm = get_llm_chatbot_default()

        if user_option == "longer":
            prompt = Prompts.editor_longer(state)
        elif user_option == "ontab":
            # tab 建操作
            prompt = Prompts.editor_ontab(state)
        elif user_option == "conver_image":
            # 封面图片生成
            pass
        else:
            prompt = Prompts.editor_improve(state)

        ai_message = await llm.ainvoke(prompt, config)
        return {
            "messages": [
                new_user_message,
                ai_message,
            ],
        }
