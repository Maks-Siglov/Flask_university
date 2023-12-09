import json

import pytest

from app.configs import API_PREFIX
from app.init_routers import (
    COURSE_POST_ROUTE,
    COURSES_ROUTE,
)

COURSES_ROUTE = f"{API_PREFIX}{COURSES_ROUTE}"
COURSE_POST_ROUTE = f"{API_PREFIX}{COURSE_POST_ROUTE}"


def test_courses(client):
    response = client.get(COURSES_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "name" in item
        assert "description" in item
        assert "students" not in item


def test_courses_with_students(client):
    response = client.get(COURSES_ROUTE, query_string={"with": "students"})
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "students" in item


GET_COURSE_ID = 1


def test_get_course(client):
    response = client.get(f"{API_PREFIX}/course/{GET_COURSE_ID}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "name" in data
    assert "description" in data
    assert "students" in data


post_course_json_cases = [
    {
        "name": "New Course",
        "description": "Educational course",
        "student_ids": [12, 13],
    },
    {
        "name": "Second new course",
        "description": " Second educational course",
        "student_ids": [14],
    },
]


@pytest.mark.parametrize("post_course_json", post_course_json_cases)
def test_post_course(client, post_course_json):
    response = client.post(COURSE_POST_ROUTE, json=post_course_json)
    assert response.status_code == 201

    new_course_name = post_course_json["name"]
    new_course_description = post_course_json["description"]
    new_course_student_ids = post_course_json["student_ids"]

    response_data = json.loads(response.data)

    assert response_data["name"] == new_course_name
    assert response_data["description"] == new_course_description
    assert len(response_data["students"]) == len(new_course_student_ids)


post_course_without_students_json = {
    "name": "Third Course",
    "description": "Third educational course",
}


def test_post_course_without_student_ids(client):
    response = client.post(
        COURSE_POST_ROUTE, json=post_course_without_students_json
    )
    assert response.status_code == 201

    new_course_name = post_course_without_students_json["name"]
    new_course_description = post_course_without_students_json["description"]

    response_data = json.loads(response.data)

    assert response_data["name"] == new_course_name
    assert response_data["description"] == new_course_description


PATCH_COURSE_ID = 1

update_course_json = {
    "name": "Updated course",
    "description": "Updated description",
}


def test_update_course(client):
    response = client.patch(
        f"{API_PREFIX}/course/{PATCH_COURSE_ID}", json=update_course_json
    )
    assert response.status_code == 200

    response_data = json.loads(response.data)

    assert response_data["name"] == update_course_json["name"]
    assert response_data["description"] == update_course_json["description"]


UPDATE_COURSE_ID = 4
append_students_json = {"student_ids": [15, 16]}


def test_course_add_students(client):
    response = client.patch(
        f"{API_PREFIX}/course/{UPDATE_COURSE_ID}/append",
        json=append_students_json,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["students"]) == len(
        append_students_json["student_ids"]
    )


REMOVE_STUDENT_COURSE_ID = 1
remove_students_json = {"student_ids": [1]}


def test_course_remove_students(client):
    response = client.patch(
        f"{API_PREFIX}/course/{REMOVE_STUDENT_COURSE_ID}/remove",
        json=remove_students_json,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["students"]) == 0


PUT_COURSE_ID = 1

put_course_json = {
    "name": "Updated put course",
    "description": "Updated put description",
    "student_ids": [15, 16, 17],
}


def test_put_course(client):
    response = client.put(
        f"{API_PREFIX}/course/{PUT_COURSE_ID}", json=put_course_json
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["name"] == put_course_json["name"]
    assert response_data["description"] == put_course_json["description"]
    assert len(response_data["students"]) == len(
        put_course_json["student_ids"]
    )


DELETE_COURSE_ID = 5


def test_delete_course(client):
    response = client.delete(f"{API_PREFIX}/course/{DELETE_COURSE_ID}")
    assert response.status_code == 204
    assert response.data == b""
