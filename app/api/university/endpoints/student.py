from typing import Any
from flask import (
    Response,
    request
)
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.models import StudentRequest

from app.crud.university.student import (
    get_all_students,
    add_student,
    delete_student,
    get_student,
)


class Students(Resource):
    def get(self) -> list[dict[str, Any]] | Response:
        """
        This method returns all students with their courses and groups
        ---
        responses:
          200:
            description: returns all students with their relations
          204:
            description: there is no students
        """
        students = get_all_students()
        if not students:
            return Response([], 204)
        return [student.to_dict() for student in students]


class Student(Resource):
    def get(self, student_id: int) -> Response | dict[str, Any]:
        """
        This method return data about student by it id
        ---
        parameters:
          - name: student_id
            in: path
            type: int
        responses:
          200:
            description: return data about student in dict
            examples: {
                    "id": 51,
                    "first_name": "Rachel",
                    "last_name": "Robinson",
                    "courses": [
                    "group": {
                          "id": 3,
                          "name": "OC-60"
                        },
                        {
                          "id": 5,
                          "name": "Mathematics",
                          "description": "Fundamental concepts of mathematics."
                        }
                        ]
                    }
          404:
            description: Student with provided id don't exist
        """
        student = get_student(student_id)
        if not student:
            return Response(f"Student with id {student_id} don't exist", 404)
        return student.to_dict()

    def post(self) -> Response:
        """
        This method add a new student to the database
        ---
        parameters:
          - name: first_name
            in: body
            type: string
          - name: last_name
            in: body
            type: string
        responses:
          201:
            description: Student added successfully
          422:
            description: Invalid types in requests
        """
        try:
            student = StudentRequest(**request.get_json())
            student_id = add_student(student)
        except ValidationError as exc:
            return Response(f'Not valid data, {exc}', status=422)

        return Response(f'id = {student_id}', status=201)

    def delete(self, student_id: int) -> Response:
        """
        This method remove student from database by student_id
        ---
        parameters:
          - name: student_id
            in: path
            type: int
        responses:
          204:
            description: Student removed successfully
          404:
            description: Student don't exist
        """
        if not get_student(student_id):
            return Response(f"Student {student_id} don't exist", status=404)

        delete_student(student_id)
        return Response(None, status=204)
