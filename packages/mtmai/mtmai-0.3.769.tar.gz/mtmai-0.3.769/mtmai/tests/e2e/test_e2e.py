import pytest
from fastapi.testclient import TestClient

from mtmai.cli.serve import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    return client


# @pytest.mark.asyncio()
# async def test_read_root():
#     async with httpx.AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/")
#     assert response.status_code == 404
# assert response.json() == {"message": "Hello World"}


# @pytest.mark.asyncio()
# async def test_read_item():
#     async with httpx.AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/items/42?q=test")
#     assert response.status_code == 200
#     assert response.json() == {"item_id": 42, "q": "test"}
