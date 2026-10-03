from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.schemas.task import CreateTaskRequest, TaskResponse

FINISHED_AT = datetime(2026, 2, 1, tzinfo=UTC)


def make_task_orm(**overrides) -> SimpleNamespace:
    defaults = {
        "id": uuid4(),
        "goal_id": uuid4(),
        "title": "Задача",
        "description": "Описание задачи",
        "is_completed": False,
        "user_id": uuid4(),
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        "updated_at": None,
        "finished_at": None,
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.mark.parametrize(
    ("title", "expected_title"),
    [
        pytest.param("Задача", "Задача", id="short-title"),
        pytest.param("a" * 40, "a" * 40, id="title-max-length-40"),
    ],
)
def test_create_task_request_valid(title, expected_title):
    goal_id = uuid4()

    request = CreateTaskRequest.model_validate(
        {"goal_id": goal_id, "title": title, "description": "Описание"}
    )

    assert request.goal_id == goal_id
    assert request.title == expected_title
    assert request.description == "Описание"


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"goal_id": uuid4(), "title": "a" * 41, "description": "d"},
            id="title-longer-than-40",
        ),  
        pytest.param(
            {"goal_id": uuid4(), "title": "Задача"},
            id="description-missing",
        ),
        pytest.param(
            {"title": "Задача", "description": "d"},
            id="goal-id-missing",
        ),
        pytest.param(
            {"goal_id": "not-a-uuid", "title": "Задача", "description": "d"},
            id="goal-id-not-a-uuid",
        ),
    ],
)
def test_create_task_request_invalid(payload):
    with pytest.raises(ValidationError):
        CreateTaskRequest.model_validate(payload)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        pytest.param(
            {},
            {"is_completed": False, "updated_at": None, "finished_at": None},
            id="optional-fields-default-to-none",
        ),
        pytest.param(
            {"is_completed": True, "updated_at": FINISHED_AT, "finished_at": FINISHED_AT},
            {"is_completed": True, "updated_at": FINISHED_AT, "finished_at": FINISHED_AT},
            id="completed-task-with-timestamps",
        ),
    ],
)
def test_task_response_from_attributes(overrides, expected):
    orm_obj = make_task_orm(**overrides)

    response = TaskResponse.model_validate(orm_obj)

    assert response.id == orm_obj.id
    assert response.goal_id == orm_obj.goal_id
    assert response.title == orm_obj.title
    assert response.description == orm_obj.description
    assert response.user_id == orm_obj.user_id
    assert response.created_at == orm_obj.created_at
    for field, value in expected.items():
        assert getattr(response, field) == value


@pytest.mark.parametrize(
    "is_completed",
    [
        pytest.param(["yes"], id="is-completed-is-a-list"),
        pytest.param({"yes": True}, id="is-completed-is-a-dict"),
        pytest.param(object(), id="is-completed-is-an-object"),
    ],
)
def test_task_response_invalid_is_completed(is_completed):
    payload = {
        "id": uuid4(),
        "goal_id": uuid4(),
        "title": "Задача",
        "description": "d",
        "is_completed": is_completed,
        "user_id": uuid4(),
        "created_at": datetime.now(UTC),
    }

    with pytest.raises(ValidationError):
        TaskResponse.model_validate(payload)
