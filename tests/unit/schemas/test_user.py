from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.schemas.user import RegisterUserRequest, UserResponse


def make_user_orm(**overrides) -> SimpleNamespace:
    defaults = {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "test",
        "hashed_password": b"hashed",
        "is_active": True,
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        pytest.param(
            {"email": "test@example.com", "username": "test", "password": "supersecret"},
            {"email": "test@example.com", "username": "test", "password": "supersecret"},
            id="valid-credentials",
        ),
        pytest.param(
            {"email": "test@example.com", "username": "test", "password": "a" * 8},
            {"password": "a" * 8},
            id="password-min-length-8",
        ),
        pytest.param(
            {"email": "test@example.com", "username": "u" * 50, "password": "supersecret"},
            {"username": "u" * 50},
            id="username-max-length-50",
        ),
    ],
)
def test_register_user_request_valid(payload, expected):
    request = RegisterUserRequest.model_validate(payload)

    for field, value in expected.items():
        assert getattr(request, field) == value


@pytest.mark.parametrize(
    "email",
    [
        pytest.param("plainaddress", id="email-without-at"),
        pytest.param("missing-at@", id="email-without-domain"),
        pytest.param("@no-local.com", id="email-without-local-part"),
        pytest.param("a b@example.com", id="email-with-space"),
        pytest.param("", id="email-empty"),
    ],
)
def test_register_user_request_invalid_email(email):
    with pytest.raises(ValidationError):
        RegisterUserRequest.model_validate(
            {"email": email, "username": "test", "password": "supersecret"}
        )


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"email": "test@example.com", "username": "", "password": "supersecret"},
            id="username-empty",
        ),
        pytest.param(
            {"email": "test@example.com", "username": "u" * 51, "password": "supersecret"},
            id="username-longer-than-50",
        ),
        pytest.param(
            {"email": "test@example.com", "username": "test", "password": "a" * 7},
            id="password-shorter-than-8",
        ),
        pytest.param(
            {"email": "test@example.com", "username": "test"},
            id="password-missing",
        ),
    ],
)
def test_register_user_request_invalid(payload):
    with pytest.raises(ValidationError):
        RegisterUserRequest.model_validate(payload)


def test_user_response_from_attributes():
    orm_obj = make_user_orm()

    response = UserResponse.model_validate(orm_obj)

    assert response.id == orm_obj.id
    assert response.email == orm_obj.email
    assert response.username == orm_obj.username
    assert response.is_active is True
    assert response.created_at == orm_obj.created_at


def test_user_response_hashed_password_not_exposed():
    response = UserResponse.model_validate(make_user_orm())

    assert "hashed_password" not in response.model_dump()
    assert not hasattr(response, "hashed_password")


@pytest.mark.parametrize(
    "overrides",
    [
        pytest.param({"email": "not-an-email"}, id="email-invalid"),
        pytest.param({"is_active": "active"}, id="is-active-not-a-bool"),
    ],
)
def test_user_response_invalid(overrides):
    payload = {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "test",
        "is_active": True,
        "created_at": datetime.now(UTC),
    }
    payload.update(overrides)

    with pytest.raises(ValidationError):
        UserResponse.model_validate(payload)
