import pytest
import json

from app.configs import API_PREFIX
from app.init_routers import (
    COURSES_ROUTE,
    COURSE_POST_ROUTE,
)
from app.crud.university.course import get_course, get_course_by_name

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
    response = client.get(COURSES_ROUTE, query_string={"with_students": True})
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "students" in item


def test_get_course(client):
    response = client.get(f"{API_PREFIX}/course/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "name" in data
    assert "description" in data
    assert "students" in data


post_course_json_cases = [
    {
        "name": "New Course",
        "description": "Educational course",
        "student_ids": [1, 2, 3],
    },
    {
        "name": "Second new course",
        "description": " Second educational course",
        "student_ids": [],
    },
]


@pytest.mark.parametrize("post_course_json", post_course_json_cases)
def test_post_course(client, post_course_json):
    response = client.post(COURSE_POST_ROUTE, json=post_course_json)
    assert response.status_code == 201

    new_course_name = post_course_json["name"]
    new_course_description = post_course_json["description"]
    new_course_student_ids = post_course_json["student_ids"]

    new_course = get_course_by_name(new_course_name)
    assert new_course.name == new_course_name
    assert new_course.description == new_course_description
    assert len(new_course.students) == len(new_course_student_ids)


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

    new_course = get_course_by_name(new_course_name)
    assert new_course.name == new_course_name
    assert new_course.description == new_course_description


PATCH_COURSE_ID = 1
UPDATE_COURSE_NANE = "Updated course"
UPDATE_COURSE_DESCRIPTION = "Updated description"

update_course_json = {
    "name": UPDATE_COURSE_NANE,
    "description": UPDATE_COURSE_DESCRIPTION,
}


def test_update_course(client):
    response = client.patch(
        f"{API_PREFIX}/course/{PATCH_COURSE_ID}", json=update_course_json
    )
    assert response.status_code == 200
    updated_course = get_course(PATCH_COURSE_ID)
    assert updated_course.name == UPDATE_COURSE_NANE
    assert updated_course.description == UPDATE_COURSE_DESCRIPTION


append_students_json = {"student_ids": [1, 2, 3]}
STUDENTS_AMOUNT = 3
UPDATE_COURSE_ID = 3


def test_course_append_students(client):
    response = client.patch(
        f"{API_PREFIX}/course/{UPDATE_COURSE_ID}/append",
        json=append_students_json,
    )
    assert response.status_code == 200
    updated_course = get_course(UPDATE_COURSE_ID)
    assert len(updated_course.students) == STUDENTS_AMOUNT


def test_course_append_duplicated_students(client):
    client.patch(
        f"{API_PREFIX}/course/{UPDATE_COURSE_ID}/append",
        json=append_students_json,
    )
    pytest.raises(ValueError)


remove_students_json = {"student_ids": [1, 2, 3]}


def test_course_remove_students(client):
    response = client.patch(
        f"{API_PREFIX}/course/{UPDATE_COURSE_ID}/remove",
        json=remove_students_json,
    )
    assert response.status_code == 200
    updated_course = get_course(UPDATE_COURSE_ID)
    assert len(updated_course.students) == 0


def test_course_remove_not_existed_students(client):
    client.patch(
        f"{API_PREFIX}/course/{UPDATE_COURSE_ID}/remove",
        json=remove_students_json,
    )
    pytest.raises(ValueError)


PUT_COURSE_NAME = "Updated put course"
PUT_COURSE_DESCRIPTION = "Updated put description"
PUT_COURSE_STUDENTS_AMOUNT = 3

put_course_json = {
    "name": PUT_COURSE_NAME,
    "description": PUT_COURSE_DESCRIPTION,
    "student_ids": [1, 2, 3],
}


def test_put_course(client):
    response = client.put(f"{API_PREFIX}/course/1", json=put_course_json)
    assert response.status_code == 200
    putted_course = get_course_by_name(PUT_COURSE_NAME)
    assert putted_course.name == PUT_COURSE_NAME
    assert putted_course.description == PUT_COURSE_DESCRIPTION
    assert len(putted_course.students) == 3


DELETE_COURSE_ID = 5


def test_delete_course(client):
    response = client.delete(f"/api/v1/course/{DELETE_COURSE_ID}")
    assert response.status_code == 204
    assert response.data == b""
