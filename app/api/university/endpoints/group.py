from typing import Any
from flask import Response
from flask_restful import Resource

from app.crud.university import less_or_equal_students_in_group


class SelectGroup(Resource):
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
        query_result = less_or_equal_students_in_group(student_amount)
        if not query_result:
            return Response('There is no group with that amount', 404)
        return [group.to_dict(exclude={'students'}) for group in query_result]
