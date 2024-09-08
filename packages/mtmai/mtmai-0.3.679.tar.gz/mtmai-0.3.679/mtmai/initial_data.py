import logging

from sqlmodel import Session

from mtmai.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
