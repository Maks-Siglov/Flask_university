import pytest

from app.configs import API_PREFIX
from app.init_routers import STUDENT_POST_ROUTE

STUDENT_POST_ROUTE = f'{API_PREFIX}{STUDENT_POST_ROUTE}'

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
    assert response.status_code == 201
    assert 'id'.encode() in response.data


remove_student_by_id_case = [2, 3]


@pytest.mark.parametrize('student_id', remove_student_by_id_case)
def test_remove_student(client, student_id):
    response = client.delete(f'/api/v1/student/{student_id}')
    assert response.status_code == 204
    assert response.data == b''


def test_remove_un_exist_student(client, student_id=100):
    response = client.delete(f'/api/v1/student/{student_id}')
    assert response.status_code == 404
