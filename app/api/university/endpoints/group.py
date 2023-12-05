from typing import Any
from flask import (
    Response,
    request,
)
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.models import (
    GroupRequest,
    GroupResponse,
)
from app.crud.university.group import (
    less_or_equal_students_in_group,
    get_all_groups,
    get_group,
    add_group,
    update_group,
    delete_group,
    overwrite_group,
)


class GroupStudentAmountApi(Resource):
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
            return Response("There is no group with that amount", 404)
        return [
            GroupResponse.model_validate(group).model_dump()
            for group in groups
        ]


class GroupsApi(Resource):
    def get(self) -> list[dict[str, Any]] | list:
        """
        This method returns all groups with their students
        ---
        responses:
          200:
            description: returns all groups or empty list if entity don't exist
        """
        with_students = request.args.get(
            "with_students", default=False, type=bool
        )
        exclude = {} if with_students else {"students"}
        groups = get_all_groups()
        return [
            GroupResponse.model_validate(group).model_dump(exclude=exclude)
            for group in groups
        ]


class GroupApi(Resource):
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
            group_data = GroupRequest(**request.get_json())
            group = add_group(group_data)
        except ValidationError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        return Response(
            GroupResponse.model_validate(group).model_dump_json(), 201
        )

    def patch(self, group_id: int, action: str | None = None):
        """
        This method update group in the database by group_id
        ---
        parameters:
          - name: group_id
            in: path
            type: int
          - name: action
            in: path
            type: str
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

        try:
            request_data = GroupRequest(**request.get_json())
        except ValueError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        update_group(group, request_data, action)
        return Response(
            f"Group with id {group_id} updated successfully", status=200
        )

    def put(self, group_id: int):
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

        try:
            request_data = GroupRequest(**request.get_json())
            request_data.check_not_none_field()
        except ValueError as exc:
            return Response(f"Not valid data, {exc}", status=422)

        overwrite_group(group, request_data)
        return Response(
            f"Group with id {group_id} updated successfully", status=200
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
        group = get_group(group_id)
        if not group:
            return Response(f"Group {group_id} don't exist", status=404)

        delete_group(group)
        return Response(None, status=204)
