"""
爬虫相关api

"""

import asyncio
import logging

from fastapi import APIRouter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from opentelemetry import trace
from pydantic import BaseModel
from scrapegraphai.graphs import SmartScraperMultiGraph

from mtmai.api.deps import SessionDep
from mtmai.core.config import settings
from mtmai.mtlibs.mtmcrawler.mtmcrawler import MTMCrawlerSiteParams, crawl_site
from mtmai.toolsv2.readable import get_readable_text

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()

router = APIRouter()


@router.get("/test_local_browser")
async def test_selenium_1():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.set_capability("browserVersion", "100")
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub", options=chrome_options
    )
    driver.get("https://www.bing.com")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Get the page title
    page_title = driver.title
    return {"title": page_title}


@router.get("/start_selenium_server")
async def start_selenium_server():
    """启动 selenium grid"""
    import asyncio

    from mtmai.mtlibs.server.selenium import (
        start_selenium_server as run_selenium_server,
    )

    asyncio.create_task(run_selenium_server())
    return {"ok": True}


@router.get("/test_easy_spider_demo1")
async def test_easy_spider_demo1():
    """启动 selenium grid"""
    import asyncio

    from mtmai.mtlibs.server.selenium import (
        start_selenium_server as run_selenium_server,
    )

    asyncio.create_task(run_selenium_server())
    return {"ok": True}


@router.get("/start_easy_spider_ui")
async def start_easy_spider_ui():
    """启动 selenium grid"""
    from mtmai.mtlibs.server.easyspider import run_easy_spider_ui

    asyncio.create_task(run_easy_spider_ui())
    return {"ok": True}


class ScrapeGraphAiReq(BaseModel):
    prompt: str
    url: str


@router.post("/mtmcrawler_scrapgraph_demo", response_model=ScrapeGraphAiReq)
def mtmcrawler_scrapgraph_demo(req: ScrapeGraphAiReq):
    # Define the configuration for the scraping pipeline
    # graph_config = {
    #     "model_instance": llm_model_instance,
    #     "embedder_model_instance": embedder_model_instance,
    #     "verbose": True,
    #     "headless": False,
    # }
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm_model_instance = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_length=128,
        temperature=0.5,
        api_key=settings.HUGGINGFACEHUB_API_TOKEN,
        # token=settings.HUGGINGFACEHUB_API_TOKEN,
    )

    embedder_model_instance = HuggingFaceInferenceAPIEmbeddings(
        api_key=settings.HUGGINGFACEHUB_API_TOKEN,
        model_name="sentence-transformers/all-MiniLM-l6-v2",
    )

    graph_config = {
        "llm": {"model_instance": llm_model_instance, "model_tokens": 2000},
        "verbose": True,
        "headless": False,
    }

    # Create the SmartScraperGraph instance
    # smart_scraper_graph = SmartScraperGraph(
    #     prompt="Find some information about what does the company do, the name and a contact email.",
    #     source="https://scrapegraphai.com/",
    #     config=graph_config,
    # )

    multiple_search_graph = SmartScraperMultiGraph(
        prompt="Who is Marco Perini?",
        source=["https://perinim.github.io/", "https://perinim.github.io/cv/"],
        schema=None,
        config=graph_config,
    )

    result = multiple_search_graph.run()
    # result = search_graph.run()
    print(result)

    # Run the pipeline
    # result = search_graph.run()
    return result


class ScraperReadableReq(BaseModel):
    url: str


@router.post("/readable")
async def test_readable(req: ScraperReadableReq):
    content = get_readable_text(req.url)
    return content


@router.post("/crawl_site")
async def crawl_site_api(db: SessionDep):
    """
    用爬虫对特定网址进行抓取，并建立索引
    """

    # 开发阶段，特定参数固定
    site_id = "1"
    url = "https://top.aibase.com/tool/screenshot-to-code"
    await crawl_site(db, MTMCrawlerSiteParams(site_id=site_id, entry_urls=[url]))
    return {
        "ok": True,
        "site_id": site_id,
    }
