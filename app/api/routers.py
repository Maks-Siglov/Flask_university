

from flask_restful import(
    Resource,
    reqparse,
)

from app.crud.sql import (
    less_or_equal_students_in_group,
    course_students,
    add_student,
    delete_student,
    add_student_to_course,
    remove_student_from_course,

)

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, location='args')
parser.add_argument('last_name', type=str, location='args')
parser.add_argument('student_amount', type=int, location='args')
parser.add_argument('course', type=str, location='args')
parser.add_argument('student_id', type=int, location='args')


class SelectGroup(Resource):
    def get(self):
        args = parser.parse_args()
        student_amount = args.get('student_amount')
        result = less_or_equal_students_in_group(student_amount)
        res = {group.id: group.name for group in result}
        return {'less or equal': res}


class CourseStudents(Resource):
    def get(self):
        args = parser.parse_args()
        course_name = args.get('course')
        result = course_students(course_name)
        res = [[student.first_name, student.last_name] for student in result]
        return {course_name: res}


class AddStudent(Resource):
    def post(self):
        args = parser.parse_args()
        first_name = args.get('first_name')
        last_name = args.get('last_name')

        add_student(first_name, last_name)

        return f'Student {first_name} {last_name} added successfully'


class DeleteStudent(Resource):
    def post(self):
        args = parser.parse_args()
        student_id = args.get('student_id')
        delete_student(student_id)

        return f'Student with id {student_id} deleted successfully'


class AddStudentToCourse(Resource):
    def post(self):
        args = parser.parse_args()
        student_id = args.get('student_id')
        course_name = args.get('course')

        add_student_to_course(student_id, course_name)

        return f'Student with id {student_id} added to {course_name}'


class RemoveStudentFromCourse(Resource):
    def post(self):
        args = parser.parse_args()
        student_id = args.get('student_id')
        course_name = args.get('course')

        remove_student_from_course(student_id, course_name)

        return f'Student with id {student_id} deleted from {course_name}'
