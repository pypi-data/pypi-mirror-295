"""
前端机器人脚本
"""

import os

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

from mtmai.core.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/main.js", include_in_schema=False)
def bot_script():
    """前端机器人脚本"""
    bot_script_path = "packages/mtmaibot/dist/main.js"
    if not os.path.exists(bot_script_path):
        logger.error(f"Bot script not found: {bot_script_path}")
        return Response(status_code=404, content="File not found")
    return FileResponse(bot_script_path)
