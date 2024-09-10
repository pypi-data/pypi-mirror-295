import logging
from typing import Optional

import fastapi
import httpx
import yaml
from langchain.pydantic_v1 import BaseModel

router = fastapi.APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)


def load_config(file_path):
    with open(file_path) as file:
        config = yaml.safe_load(file)
    return config


class Person(BaseModel):
    """Identifying information about a person in a text."""

    person_name: str
    person_height: Optional[int]  # noqa: UP007
    person_hair_color: Optional[str]  # noqa: UP007
    dog_breed: Optional[str]  # noqa: UP007
    dog_name: Optional[str]  # noqa: UP007

    class Config:  # noqa: D106
        arbitrary_types_allowed = True


def get_html_content(url: str) -> str:
    try:
        response = httpx.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
    return ""


# async def run_playwright(target_url):
#     from bs4 import BeautifulSoup
#     from playwright.async_api import async_playwright

#     # target_url = "https://sdk.vercel.ai/docs/ai-sdk-ui/streaming-data"
#     async with async_playwright() as p:
#         # browser = await p.chromium.launch(
#         #     headless=False
#         # )  # if True, may get the error: This browser is no longer supported. Please switch to a supported browser to continue using twitter.com. You can see a list of supported browsers in our He....
#         # # browser = await p.firefox.launch(headless=False)
#         # page = await browser.new_page()
#         # # Set a timeout for navigating to the page
#         # try:
#         #     # await page.goto(site, wait_until='load', timeout=20000) # 10 secs
#         #     # await page.goto(site, wait_until='load')
#         #     await page.goto(target_url, wait_until="networkidle")
#         # except TimeoutError:
#         #     print(
#         #         "Timeout reached during page load, proceeding with available content."
#         #     )
#         # page_source = await page.content()

#         html_content = get_html_content(target_url)
#         soup = BeautifulSoup(html_content, "html.parser")
#         for script in soup(
#             ["script", "style"]
#         ):  # Remove all javascript and stylesheet code
#             script.extract()
#         text = soup.get_text()
#         # Break into lines and remove leading and trailing space on each
#         lines = (line.strip() for line in text.splitlines())
#         # Break multi-headlines into a line each
#         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#         data = "\n".join(chunk for chunk in chunks if chunk)  # Drop blank lines
#     return data
