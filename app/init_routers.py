from flask_restful import Api

from app.api.university.endpoints.group import SelectGroup
from app.api.university.endpoints.student import Student
from app.api.university.endpoints.course import (
    CourseStudents,
    StudentCourse,
)


SELECT_GROUP_ROUTE = '/api/v1/select_group/<int:student_amount>'
COURSE_STUDENTS_ROUTE = '/api/v1/course_students/<string:course_name>'
STUDENT_POST_ROUTE = '/api/v1/student'
STUDENT_DELETE_ROUTE = '/api/v1/student/<int:student_id>'
STUDENT_TO_COURSE_ROUTE = '/api/v1/student_to_course'


def init_api_routers(api: Api):
    api.add_resource(SelectGroup, SELECT_GROUP_ROUTE)
    api.add_resource(CourseStudents, COURSE_STUDENTS_ROUTE)
    api.add_resource(Student, STUDENT_POST_ROUTE, STUDENT_DELETE_ROUTE)
    api.add_resource(StudentCourse, STUDENT_TO_COURSE_ROUTE)
