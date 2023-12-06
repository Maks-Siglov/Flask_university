import pytest
import json

from app.crud.university.student import get_student
from app.configs import API_PREFIX
from app.init_routers import (
    STUDENT_POST_ROUTE,
    STUDENTS_ROUTE,
)

STUDENT_POST_ROUTE = f"{API_PREFIX}{STUDENT_POST_ROUTE}"
STUDENTS_ROUTE = f"{API_PREFIX}{STUDENTS_ROUTE}"


def test_get_students(client):
    response = client.get(STUDENTS_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "first_name" in item
        assert "last_name" in item


def test_get_student(client):
    response = client.get("/api/v1/student/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "first_name" in data
    assert "last_name" in data


post_student_json_case = [
    {
        "id": 5,
        "first_name": "David",
        "last_name": "Jack",
        "group_id": 2,
        "course_ids": [1, 2],
    },
    {
        "id": 6,
        "first_name": "Bob",
        "last_name": "Ivy",
        "group_id": 3,
        "course_ids": [2, 3],
    },
]


@pytest.mark.parametrize("json_data", post_student_json_case)
def test_post_student(client, json_data):
    response = client.post(STUDENT_POST_ROUTE, json=json_data)
    assert response.status_code == 200

    student_id = json_data["id"]
    first_name = json_data["first_name"]
    last_name = json_data["last_name"]
    group_id = json_data["group_id"]
    course_ids = json_data["course_ids"]

    new_student = get_student(student_id)
    assert new_student.first_name == first_name
    assert new_student.last_name == last_name
    assert new_student.group_id == group_id
    assert len(new_student.courses) == len(course_ids)


UPDATE_WITH_ACTION_STUDENT_ID = 5
json_data_with_action = {"group_id": 2, "course_ids": [1, 2]}


def test_update_student_with_remove(client):
    response = client.patch(
        f"api/v1/student/{UPDATE_WITH_ACTION_STUDENT_ID}/remove",
        json=json_data_with_action,
    )
    assert response.status_code == 200
    updated_student = get_student(UPDATE_WITH_ACTION_STUDENT_ID)
    assert updated_student.group_id is None
    assert len(updated_student.courses) == 0


def test_update_student_with_append(client):
    response = client.patch(
        f"api/v1/student/{UPDATE_WITH_ACTION_STUDENT_ID}/append",
        json=json_data_with_action,
    )
    assert response.status_code == 200
    updated_student = get_student(UPDATE_WITH_ACTION_STUDENT_ID)

    group_id = json_data_with_action["group_id"]
    course_ids = json_data_with_action["course_ids"]

    assert updated_student.group_id == group_id
    assert len(updated_student.courses) == len(course_ids)


UPDATE_STUDENT_ID = 2
UPDATE_STUDENT_NAME = "test_name"
UPDATE_STUDENT_LAST_NAME = "test_last_name"

update_student_json = {
    "first_name": "test_name",
    "last_name": "test_last_name",
}


def test_update_student(client):
    response = client.patch(
        f"api/v1/student/{UPDATE_STUDENT_ID}", json=update_student_json
    )
    assert response.status_code == 200
    updated_student = get_student(UPDATE_STUDENT_ID)
    assert updated_student.first_name == UPDATE_STUDENT_NAME
    assert updated_student.last_name == UPDATE_STUDENT_LAST_NAME


PUT_STUDENT_ID = 1
PUT_STUDENT_NAME = "David"
PUT_STUDENT_LAST_NAME = "Smith"
PUT_STUDENT_GROUP_ID = 2

put_student_json = {
    "first_name": PUT_STUDENT_NAME,
    "last_name": PUT_STUDENT_LAST_NAME,
    "group_id": PUT_STUDENT_GROUP_ID,
    "course_ids": [1, 2],
}


def test_put_student(client):
    response = client.put(
        f"{API_PREFIX}/student/{PUT_STUDENT_ID}", json=put_student_json
    )
    assert response.status_code == 200
    putted_student = get_student(PUT_STUDENT_ID)
    assert putted_student.first_name == PUT_STUDENT_NAME
    assert putted_student.last_name == PUT_STUDENT_LAST_NAME
    assert putted_student.group_id == PUT_STUDENT_GROUP_ID
    assert len(putted_student.courses) == 2
    course_ids = put_student_json["course_ids"]
    assert len(putted_student.courses) == len(course_ids)


DELETE_STUDENT_ID = 2


def test_remove_student(client):
    response = client.delete(f"/api/v1/student/{DELETE_STUDENT_ID}")
    assert response.status_code == 204
    assert response.data == b""
