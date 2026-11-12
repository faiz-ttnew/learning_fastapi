import pytest
from fastapi.testclient import TestClient
from main import app
from app.common.enums import UserRole
from app.schemas.auth_schema import UserResponse
from app.dependencies.auth import get_current_user

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def authenticated_client(client, monkeypatch):
    def fake_current_user():
        return UserResponse(
            id=1,
            name="Faijuddin",
            email="faiz@example.com",
            role=UserRole.USER,
            is_active=True,
        )
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        fake_current_user
    )
    return client
