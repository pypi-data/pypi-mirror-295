import asyncio
import logging
from datetime import timedelta
from typing import Annotated, Any
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordRequestForm
from mtmai.core.logging import get_logger
from mtmai.llm.llm import call_chat_completions, chat_completions_stream_generator
from mtmlib.github import get_github_user_data

from mtmai.api.deps import SessionDep, get_current_active_superuser
from mtmai.core import coreutils, security
from mtmai.core.config import settings
from mtmai.core.security import get_password_hash
from openai import OpenAI
from mtmai.curd import crud, curd_account
from mtmai.models.models import Message, NewPassword, Token
from mtmai.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
import json
from typing import TYPE_CHECKING

# import fastapi
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langsmith import traceable
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
# from openai.types.chat.completion_create_params import (
#     CompletionCreateParamsBase,
#     CompletionCreateParamsStreaming,
# )
from opentelemetry import trace
# from sqlmodel import Session

# from mtmai.agents.chatbot_agent import chatbot_agent
from mtmai.agents.langgraph_crew import graph
# from mtmai.api.routes.chat_input import get_chatinput_byid
from mtmai.core.config import settings
# from mtmai.core.db import getdb
# from mtmai.models import ChatInput, ChatMessage
# from mtmai.mtlibs import mtutils
# from mtmai.mtlibs.logging import get_logger

if TYPE_CHECKING:
    from langchain_core.messages import AIMessage


router = APIRouter()
logger = get_logger()
tracer = trace.get_tracer_provider().get_tracer(__name__)




# async def chat_crewdemo(query: str):
#     yield '0:"app starting..." \n'
#     app = graph.WorkFlow().app
#     app.invoke({"emails": ["email1"]})
#     yield '0:"app finished." \n'


# async def chat_simplepost(input: str):
#     from mtmai.teams.simple_post import simple_post

#     yield '0:"simplepost starting..." \n'
#     crew = simple_post.SimplePostCrew({"topic": input})
#     result = await crew.run()
#     yield f'0:"{result}" \n'


# async def chat_landing_page(input: str):
#     from mtmai.teams.landing_page import landing_page

#     yield '0:"landing_page starting..." \n\n'
#     crew = landing_page.LandingPageCrew(input)
#     crew.run()
#     yield '0:"landing_page finished." \n\n'

API_KEY_NAME = "Authorization"
# GROQ_BASE_URL = "https://api.groq.com/openai/v1"
# async def _resp_async_generator(messages: list[Message], model: str, max_tokens: int, temperature: float):

#     # GROQ_API_KEY="sdfasdfasdf-open-apikey"
#     # API_KEY = "1234"  # Replace with your actual API key
#     client = OpenAI(
#         api_key = settings.GROQ_API_KEY,
#         base_url = GROQ_BASE_URL
#         )

#     api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
#     # def verify_api_key(api_key: str = Depends(api_key_header)):
#     #     if api_key is None:
#     #         print("API key is missing")
#     #         raise HTTPException(status_code=403, detail="API key is missing")
#     #     if api_key != f"Bearer {API_KEY}":
#     #         print(f"Invalid API key: {api_key}")
#     #         raise HTTPException(status_code=403, detail="Could not validate API key")
#     #     print(f"API key validated: {api_key}")
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": m.role, "content": m.content} for m in messages],
#         max_tokens=max_tokens,
#         temperature=temperature,
#         stream=True
#     )

#     for chunk in response:
#         chunk_data = chunk.to_dict()
#         yield f"data: {json.dumps(chunk_data)}\n\n"
#         await asyncio.sleep(0.01)
#     yield "data: [DONE]\n\n"
# @traceable
@router.post( "/chat/completions")
async def chat_completions(request: Request):
    """以兼容 openai completions 协议的方式 反代其他 ai 提供商的 completions api"""

    request_data = await request.json()
    if request_data.get("messages"):
        if request_data.get("stream"):
            return StreamingResponse(
                chat_completions_stream_generator(
                    # **{
                    #     "messages": request_data.get("messages"),
                    #     "model": request_data.get("model"),
                    #     "max_tokens": request_data.get("max_tokens"),
                    #     "temperature": request_data.get("temperature")
                    # }
                    **request_data
                ), media_type="application/x-ndjson"
            )
        else:
            return await call_chat_completions(request_data)
    else:
        return HTTPException(status_code=503, detail="No messages provided")