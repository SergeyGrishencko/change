from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.schemas.post import CreatePostRequest, PostResponse


def make_post_orm(**overrides) -> SimpleNamespace:
    defaults = {
        "id": uuid4(),
        "goal_id": uuid4(),
        "title": "Пост",
        "content": "Содержимое поста",
        "user_id": uuid4(),
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.mark.parametrize(
    ("title", "expected_title"),
    [
        pytest.param("Пост", "Пост", id="short-title"),
        pytest.param("a" * 40, "a" * 40, id="title-max-length-40"),
    ],
)
def test_create_post_request_valid(title, expected_title):
    goal_id = uuid4()

    request = CreatePostRequest.model_validate(
        {"goal_id": goal_id, "title": title, "content": "Контент"}
    )

    assert request.goal_id == goal_id
    assert request.title == expected_title
    assert request.content == "Контент"


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"goal_id": uuid4(), "title": "a" * 41, "content": "c"},
            id="title-longer-than-40",
        ),
        pytest.param(
            {"goal_id": uuid4(), "title": "Пост"},
            id="content-missing",
        ),
        pytest.param(
            {"title": "Пост", "content": "c"},
            id="goal-id-missing",
        ),
        pytest.param(
            {"goal_id": 123, "title": "Пост", "content": "c"},
            id="goal-id-not-a-uuid",
        ),
    ],
)
def test_create_post_request_invalid(payload):
    with pytest.raises(ValidationError):
        CreatePostRequest.model_validate(payload)


def test_post_response_from_attributes():
    orm_obj = make_post_orm()

    response = PostResponse.model_validate(orm_obj)

    assert response.id == orm_obj.id
    assert response.goal_id == orm_obj.goal_id
    assert response.title == orm_obj.title
    assert response.content == orm_obj.content
    assert response.user_id == orm_obj.user_id
    assert response.created_at == orm_obj.created_at


@pytest.mark.parametrize(
    "overrides",
    [
        pytest.param({"content": None}, id="content-missing"),
        pytest.param({"created_at": "not-a-datetime"}, id="created-at-not-a-datetime"),
        pytest.param({"goal_id": "not-a-uuid"}, id="goal-id-not-a-uuid"),
    ],
)
def test_post_response_invalid(overrides):
    payload = {
        "id": uuid4(),
        "goal_id": uuid4(),
        "title": "Пост",
        "content": "c",
        "user_id": uuid4(),
        "created_at": datetime.now(UTC),
    }
    payload.update(overrides)

    with pytest.raises(ValidationError):
        PostResponse.model_validate(payload)
