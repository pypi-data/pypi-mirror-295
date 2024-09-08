import logging

from sqlalchemy import text
from sqlmodel import Session, SQLModel, func, select

from mtmai.core.config import settings
from mtmai.core.db import getdb
from mtmai.curd.crud import create_user, get_user_by_email
from mtmai.models.models import Agent, UserCreate

logger = logging.getLogger()


def _seed_agent(session: Session):
    count = session.exec(select(func.count()).select_from(Agent)).one()
    if count > 0:
        return
    agents = [
        Agent(id="demo", title="demo"),
        Agent(id="joke", title="joke"),
        Agent(id="demo_subgraph", title="demo_subgraph"),
        Agent(id="chat", title="chat"),
        Agent(id="researcher", title="researcher"),
        Agent(id="crew_demo", title="crew_demo"),
        Agent(id="langdingpage", title="langdingpage"),
        Agent(id="simplepost", title="simplepost"),
    ]
    session.add_all(agents)
    session.commit()


def _seed_users(db: Session):
    count = db.exec(select(func.count()).select_from(Agent)).one()
    if count > 0:
        return

    super_user = get_user_by_email(session=db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not super_user:
        create_user(
            session=db,
            user_create=UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            ),
        )
        # add_admin_user(db, adminuser_username, adminuser_password)

    # member_user = get_user_by_email(session=db, email="member@email.com")
    # if not member_user:
    #     create_user(
    #         session=db,
    #         user_create=UserCreate(
    #             email="member@email.com",
    #             username=testing_username,
    #             password=testing_user_password,
    #         ),
    #     )
    # add_member_user(db, testing_username, testing_user_password)


def seed_db(session: Session):
    _seed_users(session)
    _seed_agent(session)


def init_database():
    logger.warning("init db instances")
    engine = getdb()

    try:
        with engine.connect() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS pgmq;"))
            connection.commit()
    except Exception:
        logger.exception("error create postgresql extensions ")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print("sedding db ...")
        seed_db(session)
    print("sedding db finished")
