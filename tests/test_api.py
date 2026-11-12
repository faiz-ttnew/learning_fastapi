

def test_home_returns_200(client):
    response = client.get('/')

    assert response.status_code == 200
    assert "message" in response.json()

def test_profile_requires_bearer_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"

    body = response.json()
    assert body["success"] is False
    assert body["data"]["message"] == "Access token required"

def test_profile_rejects_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["data"]["message"] == "Invalid or expired access token"