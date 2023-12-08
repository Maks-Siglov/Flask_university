import json

import pytest

from app.configs import API_PREFIX
from app.crud.university.group import (
    get_group,
    get_group_by_name,
)
from app.init_routers import (
    GROUP_POST_ROUTE,
    GROUPS_ROUTE,
)

GROUP_POST_ROUTE = f"{API_PREFIX}{GROUP_POST_ROUTE}"
GROUPS_ROUTE = f"{API_PREFIX}{GROUPS_ROUTE}"

test_select_case = [5, 10, 15]


@pytest.mark.parametrize("student_amount", test_select_case)
def test_less_or_equal_students_in_group(client, student_amount):
    response = client.get(f"/api/v1/group_students_amount/{student_amount}")
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "id" in item
        assert "name" in item


ZERO_STUDENTS_AMOUNT = 0


def test_404_group(client):
    response = client.get(
        f"/api/v1/group_students_amount/{ZERO_STUDENTS_AMOUNT}"
    )
    assert response.status_code == 404


def test_get_groups(client):
    response = client.get(GROUPS_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "name" in item
        assert "students" not in item


def test_get_groups_with_students(client):
    response = client.get(GROUPS_ROUTE, query_string={"with": "students"})
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


post_group_json_cases = [
    {
        "name": "TT-23",
        "student_ids": [3],
    },
    {
        "name": "EF-56",
        "student_ids": [],
    },
]


@pytest.mark.parametrize("json_data", post_group_json_cases)
def test_add_group(client, json_data):
    response = client.post(GROUP_POST_ROUTE, json=json_data)
    assert response.status_code == 201

    new_group_name = json_data["name"]
    new_group_student_ids = json_data["student_ids"]

    new_group = get_group_by_name(new_group_name)
    assert new_group.name == new_group_name
    assert len(new_group_student_ids) == len(new_group_student_ids)


UPDATE_GROUP_ID = 1
UPDATE_GROUP_NAME = "TT-41"

update_group_json = {"name": UPDATE_GROUP_NAME}


def test_update_group(client):
    response = client.patch(
        f"api/v1/group/{UPDATE_GROUP_ID}", json=update_group_json
    )
    assert response.status_code == 200
    updated_course = get_group(UPDATE_GROUP_ID)
    assert updated_course.name == UPDATE_GROUP_NAME


student_to_group_json = {"student_ids": [1]}


def test_remove_students_from_group(client):
    response = client.patch(
        f"api/v1/group/{UPDATE_GROUP_ID}/remove", json=student_to_group_json
    )
    assert response.status_code == 200
    group = get_group(UPDATE_GROUP_ID)
    assert len(group.students) == 0


def test_append_students_to_group(client):
    response = client.patch(
        f"api/v1/group/{UPDATE_GROUP_ID}/append", json=student_to_group_json
    )
    assert response.status_code == 200
    group = get_group(UPDATE_GROUP_ID)
    assert len(group.students) == 1


PUT_GROUP_ID = 5
PUT_GROUP_NAME = "PT-22"

put_group_json = {"name": "PT-22", "student_ids": [1, 2, 3]}


def test_put_group(client):
    response = client.put(
        f"{API_PREFIX}/group/{PUT_GROUP_ID}", json=put_group_json
    )
    assert response.status_code == 200
    putted_group = get_group_by_name(PUT_GROUP_NAME)
    assert len(putted_group.students) == 3


DELETE_GROUP_ID = 5


def test_delete_group(client):
    response = client.delete(f"/api/v1/group/{DELETE_GROUP_ID}")
    assert response.status_code == 204
    assert response.data == b""
