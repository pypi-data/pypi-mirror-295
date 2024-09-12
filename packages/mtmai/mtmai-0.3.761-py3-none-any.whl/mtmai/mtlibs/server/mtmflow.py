

"""
安装 langflow 并配置
"""
from pathlib import Path

from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmlib.mtutils import bash

logger = get_logger()
langflow_repo = "https://github.com/langflow-ai/langflow"
langflow_targt_dir = str(Path(settings.storage_dir, "langflow"))


async def install_langflow():
    if not Path(langflow_targt_dir).exists():
        bash(f"git clone {langflow_repo} {langflow_targt_dir}")
    else:
        bash(f"cd {langflow_targt_dir} && git pull")

    # 安装后端
    bash(f"cd {langflow_targt_dir} && poetry install")


async def run_langflow():
    logger.info(f"🚀 TODO: Running Langflow in {langflow_targt_dir}")
    if not Path(langflow_targt_dir).exists():
        await install_langflow()

