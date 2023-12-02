import pytest
import json

from app.configs import API_PREFIX
from app.init_routers import STUDENT_TO_COURSE_ROUTE
from app.crud.university.course import (
    check_student_assigned_to_course,
    get_course
)

STUDENT_TO_COURSE_ROUTE = f'{API_PREFIX}{STUDENT_TO_COURSE_ROUTE}'

course_name_case = ['course_one_student', 'course_two_student']


@pytest.mark.parametrize('course_name', course_name_case)
def test_course_students(client, course_name):
    response = client.get(f'/api/v1/course_students/{course_name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'name' in data
    assert 'description' in data
    assert 'students' in data


def test_non_exist_course(client):
    response = client.get('/api/v1/course_students/non_exist_course')
    assert response.status_code == 404


UPDATE_COURSE_JSON = {'name': 'Math', 'description': 'Fundamental of Math'}
update_course_id_case = [1]


@pytest.mark.parametrize('course_id', update_course_id_case)
def test_update_course(client, course_id):
    response = client.patch(
        f'api/v1/course/{course_id}', json=UPDATE_COURSE_JSON
    )
    assert response.status_code == 200
    updated_course = get_course(course_id)
    assert updated_course.name == 'Math'
    assert updated_course.description == 'Fundamental of Math'


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

    student_id = REMOVE_FROM_COURSE['student_id']
    course_id = REMOVE_FROM_COURSE['course_id']
    student_course_association = check_student_assigned_to_course(
        student_id, course_id
    )

    assert student_course_association is None


def test_remove_non_existing_student_course(client):
    response = client.delete(STUDENT_TO_COURSE_ROUTE, json=REMOVE_FROM_COURSE)
    assert response.status_code == 404
