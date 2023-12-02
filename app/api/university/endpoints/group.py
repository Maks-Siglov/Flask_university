from typing import Any
from flask import (
    Response,
    request
)
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.models import (
    GroupRequest,
    GroupResponse,
    StudentGroupRequest,
)
from app.crud.university.group import (
    less_or_equal_students_in_group,
    get_all_groups,
    get_group,
    add_group,
    update_group,
    delete_group,
    check_student_assigned_to_group,
    add_student_to_group,
    remove_student_from_group,
)


class GroupStudentAmount(Resource):
    def get(self, student_amount: int) -> list[dict[str, Any]] | Response:
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
          404:
            description: There is no groups with specified amount
        """
        groups = less_or_equal_students_in_group(student_amount)
        if not groups:
            return Response('There is no group with that amount', 404)
        return [
            GroupResponse.model_validate(group).model_dump()
            for group in groups
        ]


class Groups(Resource):
    def get(self) -> list[dict[str, Any]] | list:
        """
        This method returns all groups with their students
        ---
        responses:
          200:
            description: returns all groups or empty list if entity don't exist
        """
        groups = get_all_groups()
        return [
            GroupResponse.model_validate(group).model_dump()
            for group in groups
        ]


class Group(Resource):
    def get(self, group_id: int) -> Response | dict[str, Any]:
        """
        This method return data about group by it id
        ---
        parameters:
          - name: group_id
            in: path
            type: int
        responses:
          200:
            description: return data about group in dict
            examples: {
                    "id": 1,
                    "name": "FI-63",
                    "students": [
                            {
                            "id": 2,
                            "first_name": "Emma",
                            "last_name": "Wilson"
                            }
                        ]
                    }
          404:
            description: Group with provided id don't exist
        """
        group = get_group(group_id)
        if not group:
            return Response(f"Student with id {group_id} don't exist", 404)
        return GroupResponse.model_validate(group).model_dump()

    def post(self) -> Response:
        """
        This method add a new group to the database
        ---
        parameters:
          - name: name
            in: body
            type: string
        responses:
          201:
            description: Group added successfully
          422:
            description: Invalid types in requests
        """
        try:
            group = GroupRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f'Not valid data, {exc}', status=422)

        group_id = add_group(group)
        return Response(f'id = {group_id}', status=201)

    def patch(self, group_id: int):
        """
        This method update group in the database by group_id
        ---
        parameters:
          - name: group_id
            in: path
            type: int
        responses:
          200:
            description: Group updated successfully
          404:
            description: Group don't exist
          422:
            description: Not valid data for updating
        """
        group = get_group(group_id)
        if not group:
            return Response(f"Group with id {group_id} doesn't exist", 404)

        data = request.get_json()
        try:
            data = GroupRequest(**data)
        except ValidationError as exc:
            return Response(f'Not valid data, {exc}', status=422)

        update_group(group, data)
        return Response(
            f'Group with id {group_id} updated successfully', status=200
        )

    def delete(self, group_id: int):
        """
        This method remove group from database by group_id
        ---
        parameters:
          - name: group_id
            in: path
            type: int
        responses:
          204:
            description: Group removed successfully
          404:
            description: This group don't exist
        """
        if not get_group(group_id):
            return Response(f"Group {group_id} don't exist", status=404)

        delete_group(group_id)
        return Response(None, status=204)


class StudentToGroup(Resource):
    def post(self) -> Response:
        """
        This method add student to the group
        ---
        parameters:
          - name: student_id
            in: body
            type: int
          - name: group_id
            in: body
            type: int
        responses:
          201:
            description: Student added to group successfully
          409:
            description: Student already assigned to the group
          422:
            description: Invalid types in requests
        """
        try:
            student_group_id = StudentGroupRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f'Not valid data {exc}', status=422)

        student_id = student_group_id.student_id
        group_id = student_group_id.group_id

        if check_student_assigned_to_group(student_id, group_id):
            return Response('Student already assigned to group', status=409)

        add_student_to_group(student_id, group_id)
        response_message = f'Student {student_id} added to group {group_id}'
        return Response(response_message, status=201)

    def delete(self) -> Response:
        """
        This method removes student from the group
        ---
        parameters:
          - name: student_id
            in: body
            type: int
          - name: group_id
            in: body
            type: int
        responses:
          204:
            description: Student removed from group successfully
          404:
            description: Student don't assigned to the group
          422:
            description: Invalid types in requests
        """
        try:
            student_group_id = StudentGroupRequest(**request.get_json())
        except ValidationError as exc:
            return Response(f'Not valid data {exc}', status=422)

        student_id = student_group_id.student_id
        group_id = student_group_id.group_id

        if not check_student_assigned_to_group(student_id, group_id):
            return Response("Student don't assigned to group", status=409)

        remove_student_from_group(student_id)
        response_message = (
            f'Student {student_id} removed from group {group_id}'
        )
        return Response(response_message, status=204)
