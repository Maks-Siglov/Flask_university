

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
parser.add_argument('course_name', type=str, location='args')
parser.add_argument('student_id', type=int, location='args')


class SelectGroup(Resource):
    def get(self):
        """
        This method retrieves a groups with less or equal student amount
        ---
        parameters:
          - name: student_amount
            in: query
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
        """
        args = parser.parse_args()
        student_amount = args.get('student_amount')
        query_result = less_or_equal_students_in_group(student_amount)
        return [group.to_dict() for group in query_result]


class CourseStudents(Resource):
    def get(self):
        """
        This method retrieves students which related to course"
        ---
        parameters:
          - name: course_name
            in: query
            type: string

        responses:
          200:
            description: Returns students assigned to course
            examples: {
                    'application/json': {
                        Mathematics : [
                            {
                                "id": 8,
                                "first_name": "Katherine",
                                "last_name": "Thomas",
                                "group_id": 4
                            },
                            {
                                "id": 162,
                                "first_name": "Taylor",
                                "last_name": "Jones",
                                "group_id": 9
                            }
                        ]
                    }
                }
        """
        args = parser.parse_args()
        course_name = args.get('course_name')
        result = course_students(course_name)
        return {course_name: [student.to_dict()for student in result]}


class Student(Resource):
    def post(self):
        """
        This method add a new student to the database
        ---
        parameters:
          - name: first_name
            in: query
            type: string
          - name: last_name
            in: query
            type: string
        responses:
          200:
            description: Student added successfully
        """
        args = parser.parse_args()
        first_name = args.get('first_name')
        last_name = args.get('last_name')

        add_student(first_name, last_name)

        return f'Student {first_name} {last_name} added successfully'

    def delete(self):
        """
        This method remove student from database by student_id
        ---
        parameters:
          - name: student_id
            in: query
            type: int
        responses:
          200:
            description: Student removed successfully
        """
        args = parser.parse_args()
        student_id = args.get('student_id')
        delete_student(student_id)

        return f'Student with id {student_id} deleted successfully'


class StudentCourse(Resource):
    def post(self):
        """
        This method add student to the course
        ---
        parameters:
          - name: student_id
            in: query
            type: int
          - name: course
            in: query
            type: string
        responses:
          200:
            description: Student added to course successfully
        """
        args = parser.parse_args()
        student_id = args.get('student_id')
        course_name = args.get('course')

        add_student_to_course(student_id, course_name)

        return f'Student with id {student_id} added to {course_name}'

    def delete(self):
        """
        This method removes student from the course
        ---
        parameters:
          - name: student_id
            in: query
            type: int
          - name: course
            in: query
            type: string
        responses:
          200:
            description: Student removed from course successfully
        """
        args = parser.parse_args()
        student_id = args.get('student_id')
        course_name = args.get('course')

        remove_student_from_course(student_id, course_name)

        return f'Student with id {student_id} deleted from {course_name}'
