import base64

import httpx
from fastapi import APIRouter, Path
from fastapi.responses import PlainTextResponse
from github import Auth, Github
from pydantic import BaseModel

from mtmai.core.config import settings

router = APIRouter()


class DashNavItem(BaseModel):
    label: str
    url: str


@router.get("/down/{dataset_path:path}")
def dataset_download(dataset_path: str = Path(...)):
    """数据集文件下载,(内部从 github 仓库获取数据集文件)"""
    auth = Auth.Token(settings.MAIN_GH_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo("codeh007/mtdataset")
    contents = repo.get_contents(dataset_path)
    if contents.content:
        # 直接返回了内容响应
        decoded_content = base64.b64decode(contents.content)
        g.close()
        return PlainTextResponse(content=decoded_content)
    elif contents.download_url:
        # 返回下载地址, 一般是因为内容较大
        # TODO: 流式传输和, 否则可能撑爆内存.
        resp = httpx.get(contents.download_url)
        content = resp.text
        g.close()
        return content
    msg = "github 未知的响应内容"
    raise Exception(msg)  # noqa: TRY002
