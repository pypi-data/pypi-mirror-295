import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from mtmai.api.deps import get_db
from mtmai.cli.serve import app
from mtmai.core.config import settings
from mtmai.core.db import init_db
from mtmai.core.seed import seed_db
from mtmai.tests.utils.user import authentication_token_from_email
from mtmai.tests.utils.utils import get_superuser_token_headers

os.environ["PYTEST_CURRENT_TEST"] = "1"
print(
    "testing start ========================================================================================================="
)


@pytest.fixture(scope="module")
def engine() -> Generator:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine

    print("==================================drop db")
    SQLModel.metadata.drop_all(engine)


# @pytest.fixture(scope="session")
@pytest.fixture(scope="module")
def db(engine) -> Generator:
    with Session(engine) as session:
        seed_db(session)
        init_db(session)
        yield session


def override_get_db(db: Session):
    def _override_get_db() -> Generator[Session, None, None]:
        yield db

    return _override_get_db


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db(db)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


# @pytest.fixture(name="session", scope="module")
# def session_fixture():
#     engine = create_engine(
#         "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
#     )
#     SQLModel.metadata.create_all(engine)
#     with Session(engine) as session:
#         seed_db(session)
#         yield session


# @pytest.fixture(name="client")
# def client_fixture(session: Session):
#     def get_session_override():
#         return session

#     app.dependency_overrides[get_session] = get_session_override
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


# @pytest.fixture(name="client_with_user")
# def client_with_user_fixture(session: Session):
#     """测试客户端, 带测试用户上下文"""

#     def get_session_override():
#         return session

#     app.dependency_overrides[get_session] = get_session_override

#     async def _override_get_current_active_user():
#         return User(username="testuser", email="testuser@example.com", disabled=False)

#     app.dependency_overrides[get_current_active_user] = (
#         _override_get_current_active_user
#     )

#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


# def post_with_user_password(client: TestClient, username: str, password: str):
#     register_data = {"username": username, "password": password}
#     response = client.post(f"{settings.api_prefix}/auth/register", json=register_data)
#     assert response.status_code == 200

#     login_data = {"username": username, "password": password}
#     response = client.post(f"{settings.api_prefix}/token", data=login_data)
#     assert response.status_code == 200

#     token_data = response.json()
#     access_token = token_data["access_token"]
#     headers = {"Authorization": f"Bearer {access_token}"}

#     return headers

# @pytest.fixture(scope="module")
# def client() -> Generator[TestClient, None, None]:
#     client = TestClient(app)
#     with client as c:
#         yield c


# @pytest.fixture(scope="module")
# def db() -> Session:
#     engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
#     SQLModel.metadata.create_all(engine)
#     session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     yield session()
#     session().close()


# @pytest.fixture(scope="session")
# def session(engine) -> Generator:
#     with Session(engine) as session:
#         seed_db(session)
#         init_db(session)
#         yield session
