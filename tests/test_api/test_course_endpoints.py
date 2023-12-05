import pytest
import json

from app.configs import API_PREFIX
from app.init_routers import (
    COURSES_ROUTE,
    COURSE_POST_ROUTE,
)
from app.crud.university.course import get_course, get_course_by_name

COURSES_ROUTE = f'{API_PREFIX}{COURSES_ROUTE}'
COURSE_POST_ROUTE = f'{API_PREFIX}{COURSE_POST_ROUTE}'


def test_courses(client):
    response = client.get(COURSES_ROUTE)
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert 'name' in item
        assert 'description' in item
        assert 'students' not in item


def test_courses_with_students(client):
    response = client.get(COURSES_ROUTE, query_string={'with_students': True})
    assert response.status_code == 200
    for item in json.loads(response.data):
        assert 'students' in item


def test_get_course(client):
    response = client.get(f'{API_PREFIX}/course/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'name' in data
    assert 'description' in data
    assert 'students' in data


post_course_json_cases = [
    {
        'name': 'New Course',
        'description': 'Educational course',
        'student_ids': [1, 2, 3]
    },
    {
        'name': 'Second new course',
        'description': ' Second educational course',
        'student_ids': []
    }
]


@pytest.mark.parametrize('post_course_json', post_course_json_cases)
def test_post_course(client, post_course_json):
    response = client.post(COURSE_POST_ROUTE, json=post_course_json)
    assert response.status_code == 201

    new_course_name = post_course_json['name']
    new_course_description = post_course_json['description']
    new_course_student_ids = post_course_json['student_ids']

    new_course = get_course_by_name(new_course_name)
    assert new_course.name == new_course_name
    assert new_course.description == new_course_description
    assert len(new_course.students) == len(new_course_student_ids)


post_course_without_students_json = {
        'name': 'Third Course',
        'description': 'Third educational course',
}


def test_post_course_without_student_ids(client):
    response = client.post(
        COURSE_POST_ROUTE, json=post_course_without_students_json
    )
    assert response.status_code == 201
    new_course_name = post_course_without_students_json['name']
    new_course_description = post_course_without_students_json['description']
    new_course = get_course_by_name(new_course_name)
    assert new_course.name == new_course_name
    assert new_course.description == new_course_description


update_course_json = {
    'name': 'Updated course',
    'description': 'Updated description'
}


def test_update_course(client):
    response = client.patch(f'{API_PREFIX}/course/1', json=update_course_json)
    assert response.status_code == 200
    updated_course = get_course(1)
    assert updated_course.name == 'Updated course'
    assert updated_course.description == 'Updated description'


append_students_json = {"student_ids": [1, 2, 3]}


def test_course_append_students(client):
    response = client.patch(
        f'{API_PREFIX}/course/3/append',
        json=append_students_json
    )
    assert response.status_code == 200
    updated_course = get_course(3)
    assert len(updated_course.students) == 3


def test_course_append_duplicated_students(client):
    client.patch(
        f'{API_PREFIX}/course/3/append',
        json=append_students_json
    )
    pytest.raises(ValueError)


remove_students_json = {"student_ids": [1, 2, 3]}


def test_course_remove_students(client):
    response = client.patch(
        f'{API_PREFIX}/course/3/remove',
        json=remove_students_json
    )
    assert response.status_code == 200
    updated_course = get_course(3)
    assert len(updated_course.students) == 0


def test_course_remove_not_existed_students(client):
    client.patch(
        f'{API_PREFIX}/course/3/remove',
        json=remove_students_json
    )
    pytest.raises(ValueError)


def test_delete_course(client):
    response = client.delete('/api/v1/course/5')
    assert response.status_code == 204
    assert response.data == b''
