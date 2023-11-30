from typing import Any
from flask import (
    Response,
    request
)
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.models import StudentCourserRequest
from app.crud.university.course import (
    add_student_to_course,
    course_students,
    remove_student_from_course,
    check_student_assigned_to_course,
)


class CourseStudents(Resource):
    def get(self, course_name: str) -> list[dict[str, Any]] | Response:
        """
        This method retrieves students which related to course"
        ---
        parameters:
          - name: course_name
            in: path
            type: string

        responses:
          200:
            description: Returns students assigned to course
            examples:
                    'application/json': [
                        {
                          'id': 2,
                          'first_name': 'Jacob',
                          'last_name': 'Martin'
                        },
                        {
                          'id': 2,
                          'first_name': 'Bob',
                          'last_name': 'Jackson'
                        }
                    ]
          404:
            description: There is no course with specified name
        """
        try:
            students = course_students(course_name)
        except AttributeError:
            return Response(f"Course {course_name} don't exist", 404)
        return [student.to_dict() for student in students]


class StudentToCourse(Resource):
    def post(self) -> Response:
        """
        This method add student to the course
        ---
        parameters:
          - name: student_id
            in: body
            type: int
          - name: course_id
            in: body
            type: int
        responses:
          201:
            description: Student added to course successfully
          409:
            description: Student already assigned to the course
          422:
            description: Invalid types in requests
        """
        try:
            student_course_id = StudentCourserRequest(**request.get_json())
            student_id = student_course_id.student_id
            course_id = student_course_id.course_id
        except ValidationError as exc:
            return Response(f'Not valid data {exc}', status=422)

        if check_student_assigned_to_course(student_id, course_id):
            message = (
                f'Student {student_id} already assigned to course {course_id}'
            )
            return Response(message, status=409)

        add_student_to_course(student_id, course_id)
        response_message = f'Student {student_id} added to course{course_id}'
        return Response(response_message, status=201)

    def delete(self) -> Response:
        """
        This method removes student from the course
        ---
        parameters:
          - name: student_id
            in: body
            type: int
          - name: course_id
            in: body
            type: int
        responses:
          204:
            description: Student removed from course successfully
          404:
            description: Student don't assigned to the course
          422:
            description: Invalid types in requests
        """
        try:
            student_course_id = StudentCourserRequest(**request.get_json())
            student_id = student_course_id.student_id
            course_id = student_course_id.course_id
        except ValidationError as exc:
            return Response(f'Not valid data {exc}', status=422)

        if not check_student_assigned_to_course(student_id, course_id):
            message = (
                f"Student  {student_id} don't assigned to course {course_id}"
            )
            return Response(message, status=404)

        remove_student_from_course(student_id, course_id)
        message = f'Student {student_id} removed from course {course_id}'
        return Response(message, status=204)
