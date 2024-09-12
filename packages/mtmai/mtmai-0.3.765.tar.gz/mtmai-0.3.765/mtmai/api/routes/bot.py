"""
前端机器人脚本
"""

from pathlib import Path

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

from mtmai.core import coreutils
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

    config_data = {
        "baseUrl": coreutils.backend_url_base(),
        "apiPrefix": settings.API_V1_STR,
    }
    style_url = config_data.get("baseUrl") + config_data.get("apiPrefix") + "/style.css"

    script_chunks = []
    script_chunks.append(f"const config = {config_data}; window.mtmaiConfig = config;")
    script_chunks.append(f"const styleUrl = '{style_url}';")
    script_chunks.append("""
        const linkElement = document.createElement('link');
        linkElement.rel = 'stylesheet';
        linkElement.href = styleUrl;
        document.head.appendChild(linkElement);
    """)
    script_chunks.append(bot_script_path.read_text())
    bot_script_content = "\n".join(script_chunks)

    return Response(content=bot_script_content, media_type="application/javascript")


@router.get("/style.cs", include_in_schema=False)
def bot_style():
    """前端机器人脚本样式"""
    bot_script_path = Path(settings.work_dir) / "packages/mtmaibot/dist/globals.css"
    if not bot_script_path.exists():
        logger.error(f"Bot script not found: {bot_script_path}")
        return Response(status_code=404, content="File not found")
    return FileResponse(str(bot_script_path), media_type="text/css")
