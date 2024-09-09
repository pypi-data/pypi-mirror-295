import logging

from sqlmodel import Session, create_engine, select

from mtmai.core.config import settings
from mtmai.curd import crud
from mtmai.models.models import User, UserCreate


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)


logger = logging.getLogger()
engine = None


def getdb():
    global engine
    if engine is not None:
        return engine
    env_conn_str = settings.DATABASE_URL
    if env_conn_str is None:
        raise ValueError("DATABASE_URL environment variable is not set")  # noqa: EM101, TRY003
    connection_string = str(env_conn_str).replace("postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )
    return engine


# async def agetdb():
#     global engine
#     if engine is not None:
#         return engine
#     env_conn_str = settings.DATABASE_URL
#     if env_conn_str is None:
#         raise ValueError("DATABASE_URL environment variable is not set")
#     connection_string = str(env_conn_str).replace("postgresql", "postgresql+psycopg")

#     engine = create_async_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
#     )
#     return engine


engine = getdb()


def get_session():
    engine = getdb()
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
