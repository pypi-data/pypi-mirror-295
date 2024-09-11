from mtmai.core.logging import get_logger

logger = get_logger()


class CrawlWorker:
    def __init__(self):
        self.worker = None

    def start(self):
        logger.info("🕷️ 🟢 Start MTM crawler worker ")

    def stop(self):
        logger.info("🕷️ 🛑 Stop MTM crawler worker ")
