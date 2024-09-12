import asyncio
import json
import logging
from collections.abc import AsyncGenerator, Callable

import fastapi
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from mtmai.core.config import settings

router = APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)

