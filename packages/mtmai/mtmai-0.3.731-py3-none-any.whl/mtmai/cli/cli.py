"""子命令模块"""

import logging
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger()


class Cli(BaseModel):
    """子命令"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def run(self, *args, **kwargs) -> None:
        """子命令基类, 暂无实际用途"""
        # logger.info("运行子命令")
        pass
