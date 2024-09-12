"""
前端机器人脚本
"""

from pathlib import Path

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

from mtmai.core.config import settings
from mtmai.core.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/main.js", include_in_schema=False)
def bot_script():
    """前端机器人脚本"""
    bot_script_path = Path(settings.work_dir) / "packages/mtmaibot/dist/index.js"
    if not bot_script_path.exists():
        logger.error(f"Bot script not found: {bot_script_path}")
        return Response(status_code=404, content="File not found")
    return FileResponse(str(bot_script_path), media_type="application/javascript")
