import json

import pytest

from app.configs import API_PREFIX
from app.init_routers import (
    GROUP_POST_ROUTE,
    GROUPS_ROUTE,
)

GROUP_POST_ROUTE = f"{API_PREFIX}{GROUP_POST_ROUTE}"
GROUPS_ROUTE = f"{API_PREFIX}{GROUPS_ROUTE}"

student_amount_case = [5, 10, 15]


@pytest.mark.parametrize("student_amount", student_amount_case)
def test_less_or_equal_students_in_group(client, student_amount):
    response = client.get(
        f"{API_PREFIX}/group_students_amount/{student_amount}"
    )
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert "id" in item
        assert "name" in item


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


GET_GROUP_ID = 1


def test_get_group(client):
    response = client.get(f"{API_PREFIX}/group/{GET_GROUP_ID}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "name" in data
    assert "students" in data


post_group_json_cases = [
    {
        "name": "TT-23",
        "student_ids": [6, 7],
    },
    {
        "name": "EF-56",
        "student_ids": [8],
    },
]


@pytest.mark.parametrize("json_data", post_group_json_cases)
def test_post_group(client, json_data):
    response = client.post(GROUP_POST_ROUTE, json=json_data)
    assert response.status_code == 201

    new_group_name = json_data["name"]
    new_group_student_ids = json_data["student_ids"]

    response_data = json.loads(response.data)
    assert response_data["name"] == new_group_name
    assert len(response_data["students"]) == len(new_group_student_ids)


UPDATE_GROUP_ID = 1

update_group_json = {"name": "TT-41"}


def test_update_group(client):
    response = client.patch(
        f"{API_PREFIX}/group/{UPDATE_GROUP_ID}", json=update_group_json
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["name"] == update_group_json["name"]


REMOVE_STUDENT_FOR_GROUP_ID = 1
remove_student_from_group_json = {"student_ids": [1]}


def test_remove_students_from_group(client):
    response = client.patch(
        f"{API_PREFIX}/group/{REMOVE_STUDENT_FOR_GROUP_ID}/remove",
        json=remove_student_from_group_json,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["students"]) == 0


ADD_STUDENT_TO_GROUP_ID = 6
add_student_to_group_json = {"student_ids": [9]}


def test_add_students_to_group(client):
    response = client.patch(
        f"{API_PREFIX}/group/{ADD_STUDENT_TO_GROUP_ID}",
        json=add_student_to_group_json,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["students"]) == 1


PUT_GROUP_ID = 2
put_group_json = {"name": "PT-22", "student_ids": [10, 11]}


def test_put_group(client):
    response = client.put(
        f"{API_PREFIX}/group/{PUT_GROUP_ID}", json=put_group_json
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["name"] == put_group_json["name"]
    assert len(response_data["students"]) == len(put_group_json["student_ids"])


DELETE_GROUP_ID = 7


def test_delete_group(client):
    response = client.delete(f"{API_PREFIX}/group/{DELETE_GROUP_ID}")
    assert response.status_code == 204
    assert response.data == b""


def test_zero_amount_group(client):
    response = client.get(f"{API_PREFIX}/group_students_amount/0")
    assert response.status_code == 404


test_404_method_case = ["get", "patch", "put", "delete"]


@pytest.mark.parametrize("method", test_404_method_case)
def test_404_group(client, method):
    response = getattr(client, method)(f"{API_PREFIX}/group/1000")
    assert response.status_code == 404


invalid_data_json = {"name": 1243}


test_invalid_data_method_case = ["patch", "put"]


@pytest.mark.parametrize("method", test_invalid_data_method_case)
def test_invalid_data_group(client, method):
    response = getattr(client, method)(
        f"{API_PREFIX}/group/1", json=invalid_data_json
    )
    assert response.status_code == 422


def test_invalid_post_group(client):
    response = client.post(GROUP_POST_ROUTE, json=invalid_data_json)
    assert response.status_code == 422
