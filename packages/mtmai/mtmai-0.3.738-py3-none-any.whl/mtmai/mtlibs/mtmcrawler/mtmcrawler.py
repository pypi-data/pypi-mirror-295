"""
爬虫主要的功能
"""

from sqlmodel import Session

from mtmai.core.logging import get_logger
from mtmai.models.mtcrawl import MTCrawlPage

logger = get_logger()


async def _fetch_page_html(url: str):
    """
    爬取指定页面
    """
    import httpx

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None


async def crawl_page(db: Session, site_id: str, url: str):
    """
    爬取一个页面并建立页面索引
    """
    logger.info(f"crawl_page: {url}")
    html = await _fetch_page_html(url)
    if html is None:
        return None
    logger.info(f"crawl_page: {len(html)}")

    page_item = MTCrawlPage(
        site_id=site_id,
        url=url,
        title="",
        description="",
        keywords="",
        author="fake_author",
        copyright="fake_copyright",
    )
    db.add(page_item)
    db.commit()
    return page_item
