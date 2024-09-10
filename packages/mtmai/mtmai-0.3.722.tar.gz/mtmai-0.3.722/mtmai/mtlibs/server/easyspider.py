from pathlib import Path

from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmlib.mtutils import bash

logger = get_logger()
easy_spider_repo = "https://github.com/NaiboWang/EasySpider"

easy_targt_dir = str(Path(settings.storage_dir, "easyspider"))


def install_easy_spider():
    if not Path(easy_targt_dir).exists():
        bash(f"git clone {easy_spider_repo} {easy_targt_dir}")
    else:
        bash(f"cd {easy_targt_dir} && git pull")

    if not Path(easy_targt_dir, ".venv").exists():
        if Path(easy_targt_dir, "pyproject.toml").exists():
            bash(f"cd {easy_targt_dir} && poetry install")
        elif Path(easy_targt_dir, "requirements.txt").exists():
            bash(
                f"cd {easy_targt_dir} && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
            )
        else:
            logger.error("⚠️ Easy Spider 环境不正确")


def run_easy_spider():
    logger.info(f"TODO run easy spider in {easy_targt_dir}")
    if not Path(easy_targt_dir).exists():
        logger.warning("⚠️ Easy Spider not installed, installing now...")
        install_easy_spider()
        return
    bash(f"cd {easy_targt_dir} && python easyspider.py")
