import pytest
import json

from app.init_routers import (
    STUDENT_POST_ROUTE,
    STUDENT_TO_COURSE_ROUTE,
)
from app.crud.university import check_student_assigned_to_course

test_select_case = [5, 10, 15]


@pytest.mark.parametrize('student_amount', test_select_case)
def test_less_or_equal_students_in_group(client, student_amount):
    response = client.get(f'/api/v1/select_group/{student_amount}')
    assert response.status_code == 200
    data = json.loads(response.data)
    for item in data:
        assert 'id' in item
        assert 'name' in item


def test_404_group(client):
    response = client.get('/api/v1/select_group/0')
    assert response.status_code == 404


course_name_case = ['course_one_student', 'course_two_student']


@pytest.mark.parametrize('course_name', course_name_case)
def test_course_students(client, course_name):
    response = client.get(f'/api/v1/course_students/{course_name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    for item in data:
        assert 'id' in item
        assert 'first_name' in item
        assert 'last_name' in item


def test_non_exist_course(client):
    response = client.get('/api/v1/course_students/non_exist_course')
    assert response.status_code == 404


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


ADD_STUDENT_TO_COURSE = {'student_id': 4, 'course_id': 3}


def test_add_student_to_course(client):
    response = client.post(STUDENT_TO_COURSE_ROUTE, json=ADD_STUDENT_TO_COURSE)
    assert response.status_code == 201

    student_id = ADD_STUDENT_TO_COURSE['student_id']
    course_id = ADD_STUDENT_TO_COURSE['course_id']
    student_course_association = check_student_assigned_to_course(
        student_id, course_id
    )
    assert student_course_association.student_id == student_id
    assert student_course_association.course_id == course_id


ADD_DUPLICATE_STUDENT = {'student_id': 1, 'course_id': 1}


def test_add_duplicate_student_to_course(client):
    response = client.post(STUDENT_TO_COURSE_ROUTE, json=ADD_DUPLICATE_STUDENT)
    assert response.status_code == 409


REMOVE_FROM_COURSE = {'student_id': 1, 'course_id': 1}


def test_remove_student_from_course(client):
    response = client.delete(STUDENT_TO_COURSE_ROUTE, json=REMOVE_FROM_COURSE)
    assert response.status_code == 204


def test_remove_non_existing_student_course(client):
    response = client.delete(STUDENT_TO_COURSE_ROUTE, json=REMOVE_FROM_COURSE)
    assert response.status_code == 404
