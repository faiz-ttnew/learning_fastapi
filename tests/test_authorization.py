def test_authenticated_user_can_view_profile(authenticated_client):
    response = authenticated_client.get("/auth/me")

    assert response.status_code == 200

    user = response.json()["data"]["data"]
    assert user["id"] == 1
    assert user["role"] == "user"


def test_normal_user_cannot_list_auth_users(authenticated_client):
    response = authenticated_client.get("/auth/users")

    assert response.status_code == 403
    assert response.json()["data"]["message"] == "Admin access required"
