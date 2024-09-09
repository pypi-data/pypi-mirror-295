# from fastapi.testclient import TestClient

# from mtmai.core.config import settings


# def test_submit_input_create_new_chat(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     # 创建一个新聊天
#     data = {
#         "prompt": "hello prompt",
#     }

#     response = client.post(
#         f"{settings.API_V1_STR}/chat/messages/submit",
#         headers=superuser_token_headers,
#         json=data,
#     )
#     assert response.status_code == 200
#     # result = response.json()
#     # assert "chat_id" in result
#     # assert isinstance(result["chat_id"], str)


# def test_submit_input_use_exist_chat(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     # 使用一个已存在的聊天
#     data = {
#         "chat_id": "1",
#         "prompt": "hello prompt",
#     }
#     response = client.post(
#         f"{settings.API_V1_STR}/chat/messages/submit",
#         headers=superuser_token_headers,
#         json=data,
#     )
#     assert response.status_code == 200
#     result = response.json()
#     assert "chat_id" in result
#     assert isinstance(result["chat_id"], str)
#     assert result["chat_id"] == "1"
