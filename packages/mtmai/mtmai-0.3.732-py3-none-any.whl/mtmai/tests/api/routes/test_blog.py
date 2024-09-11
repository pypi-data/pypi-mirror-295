import pytest
from fastapi.testclient import TestClient

from mtmai.core.config import settings


@pytest.mark.skip(reason="暂时跳过")
def test_create_post(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/posts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    # assert "id" in content
    # assert "owner_id" in content


# @pytest.mark.skip(reason="旧代码")
# def test_blog_post_curd(client_with_user: TestClient, session: Session):
#     """简单增删改查测试"""
#     payload = {"title": "blog_post_title", "content": "<h1>content</h1>"}

#     response = client_with_user.post(f"{settings.api_prefix }/blog/posts", json=payload)
#     assert response.status_code == 200

#     post_created = response.json()

#     response = client_with_user.get(
#         f'{settings.api_prefix }/blog/posts/{post_created["id"]}'
#     )
#     assert response.status_code == 200
#     blog_post_get = response.json()
#     assert blog_post_get["id"] == post_created["id"]

#     response = client_with_user.put(
#         f'{settings.api_prefix }/blog/posts/{blog_post_get["id"]}',
#         json={"title": "title_new", "content": "new_conent"},
#     )

#     response = client_with_user.get(
#         f'{settings.api_prefix }/blog/posts/{post_created["id"]}'
#     )
#     blog_post_detail = response.json()
#     assert blog_post_detail["title"] == "title_new"
#     assert blog_post_detail["content"] == "new_conent"

#     # 简单列表查询
#     response = client_with_user.get(f"{settings.api_prefix }/blog/posts")
#     assert response.status_code == 200
#     posts = response.json()

#     assert len(posts) == 1
