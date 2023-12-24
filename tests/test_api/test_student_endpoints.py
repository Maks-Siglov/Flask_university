import json

import pytest

from app.configs import API_PREFIX
from app.crud.university.student import get_student_by_name
from app.db.session import set_session, pop_session
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


GET_STUDENT_ID = 1


def test_get_student(client):
    response = client.get(f"{API_PREFIX}/student/{GET_STUDENT_ID}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "first_name" in data
    assert "last_name" in data


post_student_json_case = [
    {
        "first_name": "David",
        "last_name": "Jack",
        "group_id": 2,
        "course_ids": [1, 2],
    },
    {
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

    first_name = json_data["first_name"]
    last_name = json_data["last_name"]
    group_id = json_data["group_id"]
    course_ids = json_data["course_ids"]

    response_data = json.loads(response.data)
    assert response_data["first_name"] == first_name
    assert response_data["last_name"] == last_name
    assert response_data["group"]["id"] == group_id
    assert len(response_data["courses"]) == len(course_ids)


post_invalid_group_student_json = {
    "first_name": "David_Invalid_Group",
    "last_name": "Jackson",
    "group_id": 100,
}


def test_post_student_with_invalid_group(client):
    client.post(STUDENT_POST_ROUTE, json=post_invalid_group_student_json)
    set_session()
    student = get_student_by_name("David_Invalid_Group")
    assert student is None
    pop_session()


UPDATE_WITH_ADD_STUDENT_ID = 5
json_data_with_add = {"group_id": 4, "course_ids": [1, 2]}


def test_update_student_with_add(client):
    response = client.patch(
        f"api/v1/student/{UPDATE_WITH_ADD_STUDENT_ID}",
        json=json_data_with_add,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)

    group_id = json_data_with_add["group_id"]
    course_ids = json_data_with_add["course_ids"]

    assert response_data["group"]["id"] == group_id
    assert len(response_data["courses"]) == len(course_ids)


UPDATE_WITH_REMOVE_STUDENT_ID = 3
json_data_with_remove = {"group_id": 3, "course_ids": [3]}


def test_update_student_with_remove(client):
    response = client.patch(
        f"api/v1/student/{UPDATE_WITH_REMOVE_STUDENT_ID}/remove",
        json=json_data_with_remove,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["group"] is None
    assert len(response_data["courses"]) == 0


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
    response_data = json.loads(response.data)
    assert response_data["first_name"] == UPDATE_STUDENT_NAME
    assert response_data["last_name"] == UPDATE_STUDENT_LAST_NAME


PUT_STUDENT_ID = 1
PUT_STUDENT_NAME = "David"
PUT_STUDENT_LAST_NAME = "Smith"
PUT_STUDENT_GROUP_ID = 5

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

    response_data = json.loads(response.data)

    assert response_data["first_name"] == PUT_STUDENT_NAME
    assert response_data["last_name"] == PUT_STUDENT_LAST_NAME
    assert response_data["group"]["id"] == PUT_STUDENT_GROUP_ID
    course_ids = put_student_json["course_ids"]
    assert len(response_data["courses"]) == len(course_ids)


INVALID_PUT_STUDENT_ID = 18
put_student_invalid_group_json = {
    "first_name": "Invalid_put_first_name",
    "last_name": "William",
    "group_id": 100,
    "course_ids": [1, 2],
}


def test_put_student_with_invalid_group(client):
    client.put(
        f"{API_PREFIX}/student/{INVALID_PUT_STUDENT_ID}",
        json=put_student_invalid_group_json,
    )
    set_session()
    student_name = put_student_invalid_group_json["first_name"]
    student = get_student_by_name(student_name)
    assert student is None
    pop_session()


DELETE_STUDENT_ID = 5


def test_remove_student(client):
    response = client.delete(f"{API_PREFIX}/student/{DELETE_STUDENT_ID}")
    assert response.status_code == 204
    assert response.data == b""


test_404_method_case = ["get", "patch", "put", "delete"]


@pytest.mark.parametrize("method", test_404_method_case)
def test_404_student(client, method):
    response = getattr(client, method)(f"{API_PREFIX}/student/1000")
    assert response.status_code == 404


invalid_data_json = {
    "first_name": 1243,
    "last_name": [],
}


test_invalid_data_method_case = ["patch", "put"]


@pytest.mark.parametrize("method", test_invalid_data_method_case)
def test_invalid_data_student(client, method):
    response = getattr(client, method)(
        f"{API_PREFIX}/student/1", json=invalid_data_json
    )
    assert response.status_code == 422


def test_invalid_data_post_student(client):
    response = client.post(STUDENT_POST_ROUTE, json=invalid_data_json)
    assert response.status_code == 422
