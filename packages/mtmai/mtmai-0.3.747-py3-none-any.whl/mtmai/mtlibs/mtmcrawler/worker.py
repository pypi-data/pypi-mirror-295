import asyncio
import json

from mtmai.core.logging import get_logger
from mtmai.mtlibs.mq.pq_queue import AsyncPGMQueue
from mtmai.mtlibs.mtmcrawler.mtmcrawler import MTMCrawlerSiteParams

logger = get_logger()

mtm_crawl_queue = "mtm-crawl-queue"


class CrawlWorker:
    def __init__(self, mq: AsyncPGMQueue):
        self.mq = mq
        self.is_running = False

    async def start(self):
        logger.info("🕷️ 🟢 Start MTM crawler worker ")
        self.is_running = True

        asyncio.create_task(self._pull_messages())

    async def stop(self):
        logger.info("🕷️ 🛑 Stop MTM crawler worker ")
        self.is_running = False

    async def _pull_messages(self):
        await self.mq.create_queue(queue=mtm_crawl_queue)
        while self.is_running:
            msg = await self.mq.read(queue=mtm_crawl_queue)
            if msg:
                await self._handle_message(msg)
            else:
                await asyncio.sleep(1)

    async def _handle_message(self, msg):
        logger.info(f"读取到消息队列的消息 : {msg}")

    async def enqueue_url(self, site_id: str, url: str):
        params = MTMCrawlerSiteParams(site_id=site_id, entry_urls=[url])
        message = json.dumps(params.model_dump())
        await self.mq.send(mtm_crawl_queue, message)
