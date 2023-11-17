

from flask_restful import Resource, reqparse

from app.crud.sql import less_or_equal_students_in_group


class SelectGroup(Resource):
    def get(self, student_amount=15):
        result = less_or_equal_students_in_group(student_amount)
        res = {group.id: group.name for group in result}
        return {'less or equal': res}
