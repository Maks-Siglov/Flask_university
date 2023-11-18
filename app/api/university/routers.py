

from flask_restful import (
    Resource,
    reqparse,
)

from app.crud.university import (
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
        query_result = less_or_equal_students_in_group(student_amount)
        return [group.to_dict() for group in query_result]


class CourseStudents(Resource):
    def get(self):
        args = parser.parse_args()
        course_name = args.get('course')
        result = course_students(course_name)
        return {course_name: [student.to_dict()for student in result]}


class AddStudent(Resource):
    def post(self):
        args = parser.parse_args()
        first_name = args.get('first_name')
        last_name = args.get('last_name')

        add_student(first_name, last_name)

        return f'Student {first_name} {last_name} added successfully'


class DeleteStudent(Resource):
    def delete(self):
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
    def delete(self):
        args = parser.parse_args()
        student_id = args.get('student_id')
        course_name = args.get('course')

        remove_student_from_course(student_id, course_name)

        return f'Student with id {student_id} deleted from {course_name}'
