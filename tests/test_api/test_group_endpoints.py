import pytest
import json

from app.configs import API_PREFIX
from app.crud.university.group import get_group, get_group_by_name
from app.init_routers import (
    GROUP_POST_ROUTE,
    COURSES_ROUTE,
)

GROUP_POST_ROUTE = f"{API_PREFIX}{GROUP_POST_ROUTE}"
COURSES_ROUTE = f"{API_PREFIX}{COURSES_ROUTE}"

test_select_case = [5, 10, 15]


@pytest.mark.parametrize("student_amount", test_select_case)
def test_less_or_equal_students_in_group(client, student_amount):
    response = client.get(f"/api/v1/group_students_amount/{student_amount}")
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "id" in item
        assert "name" in item


def test_404_group(client):
    response = client.get("/api/v1/group_students_amount/0")
    assert response.status_code == 404


def test_get_groups(client):
    response = client.get(COURSES_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "name" in item
        assert "students" not in item


def test_get_groups_with_students(client):
    response = client.get(COURSES_ROUTE, query_string={"with_students": True})
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "name" in item
        assert "students" in item


group_id_test_case = [1, 2, 3]


@pytest.mark.parametrize("group_id", group_id_test_case)
def test_get_group(client, group_id):
    response = client.get(f"/api/v1/group/{group_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "name" in data
    assert "students" in data


group_name_test_cases = ["TT-23", "EF-56"]


@pytest.mark.parametrize("group_name", group_name_test_cases)
def test_add_group(client, group_name):
    data = {"name": group_name}
    response = client.post(GROUP_POST_ROUTE, json=data)
    assert response.status_code == 201
    group = get_group_by_name(group_name)
    assert group.name == json.loads(response.data)["name"]


post_group_with_student_json = {"name": "WW-21", "student_ids": [3]}


def test_add_group_with_students(client):
    response = client.post(GROUP_POST_ROUTE, json=post_group_with_student_json)
    assert response.status_code == 201
    group = get_group_by_name("WW-21")
    assert group.name == json.loads(response.data)["name"]
    assert len(group.students) == len(json.loads(response.data)["students"])


update_group_json = {"name": "TT-41"}


def test_update_group(client):
    response = client.patch("api/v1/group/1", json=update_group_json)
    assert response.status_code == 200
    updated_course = get_group(1)
    assert updated_course.name == "TT-41"


student_to_group_json = {"student_ids": [1]}


def test_remove_students_from_group(client):
    response = client.patch(
        "api/v1/group/1/remove", json=student_to_group_json
    )
    assert response.status_code == 200
    group = get_group(1)
    assert len(group.students) == 0


def test_append_students_to_group(client):
    response = client.patch(
        "api/v1/group/1/append", json=student_to_group_json
    )
    assert response.status_code == 200
    group = get_group(1)
    assert len(group.students) == 1


put_group_json = {"name": "PT-22", "student_ids": [1, 2, 3]}


def test_put_group(client):
    response = client.put(f"{API_PREFIX}/group/1", json=put_group_json)
    assert response.status_code == 200
    putted_group = get_group_by_name("PT-22")
    assert len(putted_group.students) == 3


def test_delete_group(client):
    response = client.delete("/api/v1/group/5")
    assert response.status_code == 204
    assert response.data == b""
