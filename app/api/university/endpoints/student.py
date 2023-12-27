import typing as t

from flask import Response, request
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.api_models.student import (
    StudentRequest,
    StudentResponse,
)
from app.crud.university.student import (
    delete_student,
    get_all_students,
    get_student,
    post_student,
    put_student,
    update_student,
)


class StudentsApi(Resource):
    def get(self) -> list[dict[str, t.Any]] | Response:
        """
        This method returns all students with their courses and groups
        ---
        tags:
          - Student
        parameters:
          - name: with
            in: query
            type: str
        responses:
          200:
            description: returns all students or empty list
            examples: [
                {
                  'id': 2,
                  'first_name': 'Jacob',
                  'last_name': 'Martin',
                  'group': {
                    "id": 1,
                    "name": "ED-34"
                    },
                    courses: [
                        {
                        "id": 7,
                        "name": "Chemistry",
                        "description": "Properties and composition of matter."
                        }
                    ]
                },
            ]
        """
        with_entity = request.args.get("with", None)
        exclude = set() if with_entity == "courses" else {"courses"}
        students = get_all_students()
        return [
            StudentResponse.model_validate(student).model_dump(exclude=exclude)
            for student in students
        ]


class StudentApi(Resource):
    def get(self, student_id: int) -> dict[str, t.Any] | Response:
        """
        This method return data about student by it id
        ---
        tags:
          - Student
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
                    "group": {
                          "id": 3,
                          "name": "OC-60"
                        },
                    "courses": [
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
        return StudentResponse.model_validate(student).model_dump()

    def post(self) -> dict[str, t.Any] | Response:
        """
        This method add a new student to the database
        ---
        tags:
          - Student
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
            student_data = StudentRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        try:
            new_student = post_student(student_data)
        except ValueError as exc:
            return Response(f"Not correct data, {exc}", status=422)

        return StudentResponse.model_validate(new_student).model_dump()

    def patch(
        self, student_id: int, action: str | None = None
    ) -> dict[str, t.Any] | Response:
        """
        This method update student in the database by student_id
        ---
        tags:
          - Student
        parameters:
          - name: student_id
            in: path
            type: int
          - name: action
            in: path
            type: str
        responses:
          200:
            description: Student updated successfully
          404:
            description: Student don't exist
          422:
            description: Not valid data for updating
        """
        student = get_student(student_id)
        if not student:
            return Response(f"Student with id {student_id} doesn't exist", 404)

        try:
            request_data = StudentRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        try:
            updated_student = update_student(student, request_data, action)
        except ValueError as exc:
            return Response(f"Not correct data, {exc}", status=422)

        return StudentResponse.model_validate(updated_student).model_dump()

    def put(self, student_id: int) -> dict[str, t.Any] | Response:
        """
        This method update student in the database by student_id
        ---
        tags:
          - Student
        parameters:
          - name: student_id
            in: path
            type: int
        responses:
          200:
            description: Student updated successfully
          404:
            description: Student don't exist
          422:
            description: Not valid data for updating
        """
        student = get_student(student_id)
        if not student:
            return Response(f"Student with id {student_id} doesn't exist", 404)

        try:
            request_data = StudentRequest(**request.get_json())
            request_data.check_not_none_field()
            putted_student = put_student(student, request_data)
        except (ValidationError, ValueError) as exc:
            return Response(f"Not valid data, {exc}", status=422)

        return StudentResponse.model_validate(putted_student).model_dump()

    def delete(self, student_id: int) -> Response:
        """
        This method remove student from database by student_id
        ---
        tags:
          - Student
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
        student = get_student(student_id)
        if not student:
            return Response(f"Student {student_id} don't exist", status=404)

        delete_student(student)
        return Response(None, status=204)
