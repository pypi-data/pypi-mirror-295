from fastapi.testclient import TestClient
from sqlmodel import Session

from mtmai.core.config import settings


def test_read_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/agent",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    # content = response.json()
    # assert len(content["data"]) >= 2
