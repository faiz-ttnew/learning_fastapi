from unittest.mock import MagicMock

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from app.core.security import create_access_token
from app.schemas.auth_schema import UserResponse
from app.services import auth_service


@pytest.fixture
def auth_headers():
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def cache_dependencies(monkeypatch):
    user = UserResponse(
        id=1,
        name="Faijuddin",
        email="faiz@example.com",
        role="user",
        is_active=True,
    )

    fake_redis = MagicMock()
    monkeypatch.setattr(auth_service, "redis_client", fake_redis)

    fake_connect = MagicMock()
    fake_connection = fake_connect.return_value.__enter__.return_value
    fake_result = fake_connection.execute.return_value
    fake_result.mappings.return_value.one_or_none.return_value = user.model_dump()

    monkeypatch.setattr(auth_service.engine, "connect", fake_connect)

    return user, fake_redis, fake_connect

def test_cache_hit_skips_mysql(client, auth_headers, cache_dependencies):
    user, fake_redis, fake_connect = cache_dependencies
    fake_redis.get.return_value = user.model_dump_json()

    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["data"]["data"]["id"] == user.id
    fake_redis.get.assert_called_once()
    fake_connect.assert_not_called()


def test_cache_miss_fetches_mysql_and_populates_cache(
    client, auth_headers, cache_dependencies
):
    user, fake_redis, fake_connect = cache_dependencies
    fake_redis.get.return_value = None

    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    fake_connect.assert_called_once()

    cache_key = f"{auth_service.AUTH_CACHE_KEY_PREFIX}:user:{user.id}"
    fake_redis.set.assert_called_once_with(
        cache_key,
        user.model_dump_json(),
        ex=auth_service.AUTH_CACHE_TTL_SECONDS,
    )


def test_redis_outage_falls_back_to_mysql(
    client, auth_headers, cache_dependencies
):
    _, fake_redis, fake_connect = cache_dependencies
    fake_redis.get.side_effect = RedisConnectionError("Redis unavailable")
    fake_redis.set.side_effect = RedisConnectionError("Redis unavailable")

    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    fake_connect.assert_called_once()
