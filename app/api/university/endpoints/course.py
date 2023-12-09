import typing as t

from flask import Response, request
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.api_models.course import (
    CourseRequest,
    CourseResponse,
)
from app.crud.university.course import (
    add_course,
    delete_course,
    get_all_courses,
    get_course,
    put_course,
    update_course,
)


class CoursesApi(Resource):
    def get(self) -> list[dict[str, t.Any]] | list:
        """
        This method returns all courses with their students
        ---
        parameters:
          - name: with
            in: query
            type: str
        responses:
          200:
            description: returns all courses or empty list
            examples: [
                    {
                    'id': 1,
                    'name': 'Chemistry',
                    "description": "Properties and composition of matter.",
                    students: [
                            {
                                'id': 2,
                                'first_name': 'Jacob',
                                'last_name': 'Martin'
                            },
                        ]
                    },
                    'id': 2,
                    'name': 'Physics',
                    "description": "Principles of matter and energy.",
                    students: []
                ]
        """
        with_entity = request.args.get("with", None)
        exclude = set() if with_entity == "students" else {"students"}
        courses = get_all_courses()
        return [
            CourseResponse.model_validate(course).model_dump(exclude=exclude)
            for course in courses
        ]


class CourseApi(Resource):
    def get(self, course_id: int) -> Response | dict[str, t.Any]:
        """
        This method return data about course by it id
        ---
        parameters:
          - name: course_id
            in: path
            type: int
        responses:
          200:
            description: return data about course in dict
            examples: {
                    "id": 4,
                    "name": "Chemistry",
                    "description": "Properties and composition of matter.",
                    "students": [
                            {
                            "id": 2,
                            "first_name": "Emma",
                            "last_name": "Wilson"
                            }
                        ]
                    }
          404:
            description: course with provided id don't exist
        """
        course = get_course(course_id)
        if not course:
            return Response(f"Course with id {course_id} don't exist", 404)
        return CourseResponse.model_validate(course).model_dump()

    def post(self) -> Response:
        """
        This method add a new course to the database
        ---
        parameters:
          - name: name
            in: body
            type: string
        responses:
          201:
            description: course added successfully
          422:
            description: Invalid types in requests
        """
        try:
            course_data = CourseRequest(**request.get_json())
            course = add_course(course_data)
        except (ValidationError, ValueError) as exc:
            return Response(f"Not valid data, {exc}", status=422)

        return Response(
            CourseResponse.model_validate(course).model_dump_json(), 201
        )

    def patch(
        self, course_id: int, action: str | None = None
    ) -> dict[str, t.Any] | Response:
        """
        This method update course in the database by course_id
        ---
        parameters:
          - name: course_id
            in: path
            type: int
          - name: action
            in: path
            type: str
        responses:
          200:
            description: Course updated successfully
          404:
            description: Course don't exist
          422:
            description: Not valid data for updating
        """
        course = get_course(course_id)
        if not course:
            return Response(f"Course with id {course_id} doesn't exist", 404)

        try:
            request_data = CourseRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        updated_course = update_course(course, request_data, action)
        return CourseResponse.model_validate(updated_course).model_dump()

    def put(self, course_id: int) -> dict[str, t.Any] | Response:
        """
        This method update entire course in the database by course_id
        ---
        parameters:
          - name: course_id
            in: path
            type: int
          - name: action
            in: path
            type: str
        responses:
          200:
            description: Course updated successfully
          404:
            description: Course don't exist
          422:
            description: Not valid data for updating
        """
        course = get_course(course_id)
        if not course:
            return Response(f"Course with id {course_id} doesn't exist", 404)

        try:
            request_data = CourseRequest(**request.get_json())
            request_data.check_not_none_field()
        except ValidationError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        putted_course = put_course(course, request_data)
        return CourseResponse.model_validate(putted_course).model_dump()

    def delete(self, course_id: int):
        """
        This method remove course from database by course_id
        ---
        parameters:
          - name: course_id
            in: path
            type: int
        responses:
          204:
            description: course removed successfully
          404:
            description: This course don't exist
        """
        course = get_course(course_id)
        if not course:
            return Response(f"course {course_id} don't exist", status=404)

        delete_course(course)
        return Response(None, status=204)
