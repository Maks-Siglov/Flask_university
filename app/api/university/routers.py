

from flask import Response, request, jsonify
from flask_restful import Resource

from app.api.university.models import StudentRequest
from app.crud.university import (
    add_student,
    add_student_to_course,
    course_students,
    delete_student,
    less_or_equal_students_in_group,
    remove_student_from_course,
    check_student_assigned_to_course,
    get_student,
)


class SelectGroup(Resource):
    def get(self, student_amount):
        """
        This method retrieves a groups with less or equal student amount
        ---
        parameters:
          - name: student_amount
            in: path
            type: int

        responses:
          200:
            description: Returns groups with less or equal student amount
            examples: {
                    'application/json': [
                        {'id': 9, 'name': 'TT-23'},
                        {'id': 3, 'name': 'CS-11'},
                    ]
                }
        """
        query_result = less_or_equal_students_in_group(student_amount)
        return [group.to_dict() for group in query_result]


class CourseStudents(Resource):
    def get(self, course_name):
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
            examples: {
                    'application/json': {
                        Mathematics : [
                            {
                                "id": 8,
                                "first_name": "Katherine",
                                "last_name": "Thomas",
                                "group_id": 4
                            },
                            {
                                "id": 162,
                                "first_name": "Taylor",
                                "last_name": "Jones",
                                "group_id": 9
                            }
                        ]
                    }
                }
        """
        students = course_students(course_name)
        return {course_name: [student.to_dict() for student in students]}


class Student(Resource):
    def post(self) -> Response:
        """
        This method add a new student to the database
        ---
        parameters:
          - name: first_name
            in: query
            type: string
          - name: last_name
            in: query
            type: string
        responses:
          201:
            description: Student added successfully
        """
        try:
            student = StudentRequest(**request.get_json())
            student_id = add_student(student)
        except TypeError as exc:
            return Response(f'Not valid data {exc}', status=422)

        return Response(f'id={student_id}', status=201)

    def delete(self, student_id: int) -> Response:
        """
        This method remove student from database by student_id
        ---
        parameters:
          - name: student_id
            in: query
            type: int
        responses:
          204:
            description: Student removed successfully
        """
        if not get_student(student_id):
            return Response(f"Student {student_id} don't exist", status=404)

        delete_student(student_id)
        return Response(None, status=204)


class StudentCourse(Resource):
    def post(self, student_id: int, course_id: int) -> Response:
        """
        This method add student to the course
        ---
        parameters:
          - name: student_id
            in: query
            type: int
          - name: course
            in: query
            type: string
        responses:
          201:
            description: Student added to course successfully
          409:
            description: Student already assigned to the course
        """
        if check_student_assigned_to_course(student_id, course_id):
            message = (
                f'Student {student_id} already assigned to course {course_id}'
            )
            return Response(message, status=409)

        add_student_to_course(student_id, course_id)
        message = f'Student {student_id} added to course{course_id}'
        return Response(message, status=201)

    def delete(self, student_id: int, course_id: int) -> Response:
        """
        This method removes student from the course
        ---
        parameters:
          - name: student_id
            in: path
            type: int
          - name: course_id
            in: path
            type: id
        responses:
          204:
            description: Student removed from course successfully
          404:
            description: Student don't assigned to the course
        """
        if check_student_assigned_to_course(student_id, course_id):
            message = (
                f"Student  {student_id} don't assigned to course {course_id}"
            )
            return Response(message, status=404)

        remove_student_from_course(student_id, course_id)
        message = f'Student {student_id} removed from course{course_id}'
        return Response(message, status=204)
