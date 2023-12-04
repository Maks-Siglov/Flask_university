import json

import pytest

from app.crud.university.student import get_student
from app.configs import API_PREFIX
from app.init_routers import (
    STUDENT_POST_ROUTE,
    STUDENTS_ROUTE,
)

STUDENT_POST_ROUTE = f'{API_PREFIX}{STUDENT_POST_ROUTE}'
STUDENTS_ROUTE = f'{API_PREFIX}{STUDENTS_ROUTE}'


def test_get_students(client):
    response = client.get(STUDENTS_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert 'first_name' in item
        assert 'last_name' in item


def test_get_student(client):
    response = client.get('/api/v1/student/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'first_name' in data
    assert 'last_name' in data


add_student_case = [
    {'first_name': 'David', 'last_name': 'Jack'},
    {'first_name': 'Bob', 'last_name': 'Ivy'},
]


@pytest.mark.parametrize('first_name, last_name', add_student_case)
def test_add_student(client, first_name, last_name):
    data = {
        'first_name': first_name,
        'last_name': last_name
    }
    response = client.post(STUDENT_POST_ROUTE, json=data)
    assert response.status_code == 200
    assert 'id'.encode() in response.data


update_student_json = {
    'first_name': 'test_name', 'last_name': 'test_last_name'
}
update_student_id_case = [2, 3]


@pytest.mark.parametrize('student_id', update_student_id_case)
def test_update_student(client, student_id):
    response = client.patch(
        f'api/v1/student/{student_id}', json=update_student_json
    )
    assert response.status_code == 200
    updated_student = get_student(student_id)
    assert updated_student.first_name == 'test_name'
    assert updated_student.last_name == 'test_last_name'


remove_student_by_id_case = [2, 3]


@pytest.mark.parametrize('student_id', remove_student_by_id_case)
def test_remove_student(client, student_id):
    response = client.delete(f'/api/v1/student/{student_id}')
    assert response.status_code == 204
    assert response.data == b''


def test_remove_un_exist_student(client, student_id=100):
    response = client.delete(f'/api/v1/student/{student_id}')
    assert response.status_code == 404
