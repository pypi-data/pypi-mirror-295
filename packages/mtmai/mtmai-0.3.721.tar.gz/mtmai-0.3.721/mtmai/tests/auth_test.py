# def test_user_register(session: Session, client: TestClient):
#     req = UserRegisterReq(username="testuser", password="password1")
#     response = client.post(
#         settings.api_prefix + "/auth/register", json=req.model_dump()
#     )
#     assert response.status_code == 200

#     user1 = session.exec(select(User).where(User.username == req.username)).first()

#     assert user1.username == req.username


# # Test case for login_for_access_token
# def test_login_for_access_token(client: TestClient, session: Session):
#     # Create a user for authentication
#     user = User(username="testuser", hashed_password=get_password_hash("password1"))
#     session.add(user)
#     session.commit()

#     # Perform login
#     response = client.post(
#         settings.api_prefix + "/token",
#         data={"username": "testuser", "password": "password1"},
#     )

#     # Check the response
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     assert "token_type" in data
#     assert data["token_type"] == "bearer"


# def test_me(client: TestClient, session: Session):
#     # 注册并获取访问令牌
#     headers = post_with_user_password(client, "testuser", "password1")

#     response = client.get(f"{settings.api_prefix }/me", headers=headers)
#     assert response.status_code == 200

#     user_data = response.json()
#     assert user_data["username"] == "testuser"
#     assert "id" in user_data
#     assert "email" in user_data


# def test_me_endpoint(client_with_user: TestClient):
#     response = client_with_user.get(f"{settings.api_prefix }/me")
#     assert response.status_code == 200

#     user_data = response.json()
#     assert user_data["username"] == "testuser"
#     assert user_data["email"] == "testuser@example.com"
