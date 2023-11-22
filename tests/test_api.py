

import pytest
import json

from app.app import (
    STUDENT_POST_ROUTE,
    STUDENT_TO_COURSE_ROUTE,
)
from app.crud.university import get_student_assigned_to_course

test_select_case = [5, 10, 25]


@pytest.mark.parametrize('group_id', test_select_case)
def test_less_or_equal_students_in_group(client, group_id):
    response = client.get(f'/api/v1/select_group/{group_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    for item in data:
        assert 'id' in item
        assert 'name' in item


course_name_case = ['Mathematics', 'Chemistry']


@pytest.mark.parametrize('course_name', course_name_case)
def test_course_students(client, course_name):
    response = client.get(f'/api/v1/course_students/{course_name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    for item in data:
        assert 'id' in item
        assert 'first_name' in item
        assert 'last_name' in item


add_student_case = [('David', 'Jack'), ('Bob', 'Ivy')]


@pytest.mark.parametrize('first_name, last_name', add_student_case)
def test_add_student(client, first_name, last_name):
    data = {
        'first_name': first_name,
        'last_name': last_name
    }
    response = client.post(STUDENT_POST_ROUTE, json=data)
    assert response.status_code == 201
    assert 'id'.encode() in response.data


remove_student_case = [1, 2, 3]


@pytest.mark.parametrize('student_id', remove_student_case)
def test_remove_student(client, student_id):
    response = client.delete(f'/api/v1/student/{student_id}')
    assert response.status_code == 204
    assert response.data == b''


def test_add_student_to_course(client):
    data = {
        'student_id': 201,
        'course_id': 1
    }
    response = client.post(STUDENT_TO_COURSE_ROUTE, json=data)
    assert response.status_code == 201

    student_id = data['student_id']
    course_id = data['course_id']
    student_course_association = get_student_assigned_to_course(
        student_id, course_id
    )
    assert student_course_association.student_id == student_id
    assert student_course_association.course_id == course_id


def test_add_duplicate_student_to_course(client):
    data = {
        'student_id': 201,
        'course_id': 1
    }
    response = client.post(STUDENT_TO_COURSE_ROUTE, json=data)
    assert response.status_code == 409


def test_remove_student_from_course(client):
    data = {
        'student_id': 201,
        'course_id': 1
    }
    response = client.delete(STUDENT_TO_COURSE_ROUTE, json=data)
    assert response.status_code == 204


def test_remove_non_existing_student_course(client):
    data = {
        'student_id': 201,
        'course_id': 1
    }
    response = client.delete(STUDENT_TO_COURSE_ROUTE, json=data)
    assert response.status_code == 404
