import pytest
import json

from app.crud.university.group import check_student_assigned_to_group
from app.init_routers import (
    GROUP_POST_ROUTE,
    STUDENT_TO_GROUP_ROUTE,
)

test_select_case = [5, 10, 15]


@pytest.mark.parametrize('student_amount', test_select_case)
def test_less_or_equal_students_in_group(client, student_amount):
    response = client.get(f'/api/v1/group_students_amount/{student_amount}')
    assert response.status_code == 200
    data = json.loads(response.data)
    for item in data:
        assert 'id' in item
        assert 'name' in item


def test_404_group(client):
    response = client.get('/api/v1/group_students_amount/0')
    assert response.status_code == 404


group_id_test_case = [1, 2, 3]


@pytest.mark.parametrize('group_id', group_id_test_case)
def test_get_group(client, group_id):
    response = client.get(f'/api/v1/group/{group_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'name' in data
    assert 'students' in data


group_name_test_cases = ['TT-23', 'EF-56']


@pytest.mark.parametrize('group_name', group_name_test_cases)
def test_add_group(client, group_name):
    data = {'name': group_name}
    response = client.post(GROUP_POST_ROUTE, json=data)
    assert response.status_code == 201
    assert 'id'.encode() in response.data


def test_delete_group(client):
    response = client.delete('/api/v1/group/5')
    assert response.status_code == 204
    assert response.data == b''


ADD_STUDENT_TO_GROUP = {'student_id': 1, 'group_id': 3}


def test_add_student_to_group(client):
    response = client.post(STUDENT_TO_GROUP_ROUTE, json=ADD_STUDENT_TO_GROUP)
    assert response.status_code == 201

    student_id = ADD_STUDENT_TO_GROUP['student_id']
    group_id = ADD_STUDENT_TO_GROUP['group_id']
    student_group_association = check_student_assigned_to_group(
        student_id, group_id
    )

    assert student_group_association.group_id == group_id


REMOVE_STUDENT_FROM_GROUP = {'student_id': 1, 'group_id': 3}


def test_remove_student_from_group(client):
    response = client.delete(
        STUDENT_TO_GROUP_ROUTE, json=REMOVE_STUDENT_FROM_GROUP
    )
    assert response.status_code == 204

    student_id = REMOVE_STUDENT_FROM_GROUP['student_id']
    group_id = REMOVE_STUDENT_FROM_GROUP['group_id']
    student_group_association = check_student_assigned_to_group(
        student_id, group_id
    )

    assert student_group_association is None
