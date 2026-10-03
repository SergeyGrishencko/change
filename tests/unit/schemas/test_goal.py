from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.enums.goal import GoalStatusEnum
from src.schemas.goal import CreateGoalRequest, GoalResponse

FINISHED_AT = datetime(2026, 2, 1, tzinfo=UTC)


def make_goal_orm(**overrides) -> SimpleNamespace:
    defaults = {
        "id": uuid4(),
        "title": "Выучить английский",
        "status": GoalStatusEnum.active,
        "user_id": uuid4(),
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        "description": None,
        "updated_at": None,
        "finished_at": None,
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_description"),
    [
        pytest.param(
            {"title": "Цель", "description": "Описание"},
            "Цель",
            "Описание",
            id="title-and-description",
        ),
        pytest.param({"title": "Цель"}, "Цель", None, id="description-defaults-to-none"),
        pytest.param({"title": "a" * 40}, "a" * 40, None, id="title-max-length-40"),
    ],
)
def test_create_goal_request_valid(payload, expected_title, expected_description):
    request = CreateGoalRequest.model_validate(payload)

    assert request.title == expected_title
    assert request.description == expected_description


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"title": "a" * 41}, id="title-longer-than-40"),
        pytest.param({}, id="title-missing"),
    ],
)
def test_create_goal_request_invalid(payload):
    with pytest.raises(ValidationError):
        CreateGoalRequest.model_validate(payload)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        pytest.param(
            {},
            {"status": GoalStatusEnum.active, "description": None, "updated_at": None, "finished_at": None},
            id="optional-fields-default-to-none",
        ),
        pytest.param(
            {
                "description": "desc",
                "updated_at": FINISHED_AT,
                "finished_at": FINISHED_AT,
                "status": GoalStatusEnum.completed,
            },
            {"status": GoalStatusEnum.completed, "description": "desc", "updated_at": FINISHED_AT, "finished_at": FINISHED_AT},
            id="all-fields-filled",
        ),
    ],
)
def test_goal_response_from_attributes(overrides, expected):
    orm_obj = make_goal_orm(**overrides)

    response = GoalResponse.model_validate(orm_obj)

    assert response.id == orm_obj.id
    assert response.title == orm_obj.title
    assert response.user_id == orm_obj.user_id
    assert response.created_at == orm_obj.created_at
    for field, value in expected.items():
        assert getattr(response, field) == value


@pytest.mark.parametrize(
    "status",
    [
        pytest.param("unknown", id="status-not-in-enum"),
        pytest.param(123, id="status-not-a-string"),
    ],
)
def test_goal_response_invalid_status(status):
    payload = {
        "id": uuid4(),
        "title": "Цель",
        "status": status,
        "user_id": uuid4(),
        "created_at": datetime.now(UTC),
    }

    with pytest.raises(ValidationError):
        GoalResponse.model_validate(payload)
