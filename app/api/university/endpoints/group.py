import typing as t

from flask import Response, request
from flask_restful import Resource
from pydantic import ValidationError

from app.api.university.api_models.group import (
    GroupRequest,
    GroupResponse,
)
from app.crud.university.group import (
    add_group,
    delete_group,
    get_all_groups,
    get_group,
    less_or_equal_students_in_group,
    put_group,
    update_group,
)


class GroupStudentAmountApi(Resource):
    def get(self, student_amount: int) -> list[dict[str, t.Any]] | Response:
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
            examples: [
                    {
                      "id": 9,
                      "name": "XH-33",
                      "students": []
                    },
                    {
                      "id": 3,
                      "name": "TN-56",
                      "students": [
                            "id": 15,
                            "first_name": "Grace",
                            "last_name": "White"
                        ]
                    },
                ]
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
    def get(self) -> list[dict[str, t.Any]] | list:
        """
        This method returns all groups with their students
        ---
        parameters:
          - name: with
            in: query
            type: str
        responses:
          200:
            description: returns all groups or empty list if entity don't exist
        """
        with_entity = request.args.get("with", None)
        exclude = set() if with_entity == "students" else {"students"}
        groups = get_all_groups()
        return [
            GroupResponse.model_validate(group).model_dump(exclude=exclude)
            for group in groups
        ]


class GroupApi(Resource):
    def get(self, group_id: int) -> Response | dict[str, t.Any]:
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

    def patch(
        self, group_id: int, action: str | None = None
    ) -> dict[str, t.Any] | Response:
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

        updated_group = update_group(group, request_data, action)
        return GroupResponse.model_validate(updated_group).model_dump()

    def put(self, group_id: int) -> dict[str, t.Any] | Response:
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

        putted_group = put_group(group, request_data)
        return GroupResponse.model_validate(putted_group).model_dump()

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
