import logging

from pydantic import BaseModel
from sqlmodel import Session, desc, select

from mtmai.models.chat import ChatInput, MtmChatMessage, MtmChatMessageBase
from mtmai.models.models import (
    Account,
)

logger = logging.getLogger()


class ChatSubmitPublic(BaseModel):
    chat_id: str | None = None
    agent_name: str
    messages: list[MtmChatMessageBase]


def submit_chat_messages(
    *, db: Session, data: ChatSubmitPublic, owner_id: str
) -> Account:
    chat_input_item = ChatInput()
    chat_input_item.agent_id = data.agent_name
    chat_input_item.user_id = owner_id
    chat_input_item.id = data.chat_id
    # if not data.chat_id:
    #     # 是全新的对话
    #     db.add(chat_input_item)
    #     db.commit()
    #     db.refresh(chat_input_item)
    #     logger.info("创建了 chat input %s", chat_input_item.id)
    # else:
    # 现有对话
    chat_input_get = get_chat_input(db, data.chat_id)
    if not chat_input_get:
        # msg = "获取 chat input 记录出错"
        # raise Exception(msg)
        # 是全新的对话
        db.add(chat_input_item)
        db.commit()
        db.refresh(chat_input_item)
        logger.info("创建了 chat input %s", chat_input_item.id)

    db.add_all(
        [
            MtmChatMessage(
                content=x.content,
                # chat=chat_input_item,
                chat_id=chat_input_item.id,
                role=x.role,
            )
            for x in data.messages
        ]
    )
    db.commit()
    return chat_input_item


def append_chat_messages(db: Session, chat_messages: list[MtmChatMessage]):
    """批量追加聊天历史"""
    logger.info("追加聊天历史, 消息数量: %d", len(chat_messages))
    db.add_all(chat_messages)


def get_chat_input(db: Session, id: str):
    statement = select(ChatInput).where(ChatInput.id == id)
    result = db.exec(statement=statement).first()
    return result


def get_conversation_messages(
    db: Session,
    conversation_id: str,
    offset: int = 0,
    limit: int = 100,
):
    """
    获取 对话的消息记录
    """
    if limit > 1000:
        msg = "limit too large"
        raise Exception(msg)  # noqa: TRY002
    if not conversation_id:
        msg = "require conversation_id"
        raise Exception(msg)  # noqa: TRY002
    chat_messages = db.exec(
        select(MtmChatMessage)
        .where(MtmChatMessage.chat_id == conversation_id)
        .order_by(desc(MtmChatMessage.created_at))
        .offset(offset)
        .limit(limit)
    ).all()

    chat_messages.reverse()
    return chat_messages
