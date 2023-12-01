from flask_restful import Api

from app.api.university.endpoints.student import (
    Students,
    Student
)
from app.api.university.endpoints.group import (
    GroupStudentAmount,
    StudentToGroup,
    Group,
    Groups,
)
from app.api.university.endpoints.course import (
    Courses,
    CourseStudents,
    StudentToCourse,
)


GROUP_STUDENTS_AMOUNT_ROUTE = (
    '/api/v1/group_students_amount/<int:student_amount>'
)
GROUPS_ROUTE = '/api/v1/groups'
GROUP_ROUTE = '/api/v1/group/<int:group_id>'
GROUP_POST_ROUTE = '/api/v1/group'
STUDENT_TO_GROUP_ROUTE = '/api/v1/student_to_group'

STUDENTS_ROUTE = '/api/v1/students'
STUDENT_POST_ROUTE = '/api/v1/student'
STUDENT_ROUTE = '/api/v1/student/<int:student_id>'

COURSES_ROUTE = '/api/v1/courses'
COURSE_STUDENTS_ROUTE = '/api/v1/course_students/<string:course_name>'
STUDENT_TO_COURSE_ROUTE = '/api/v1/student_to_course'


def init_api_routers(api: Api):
    api.add_resource(GroupStudentAmount, GROUP_STUDENTS_AMOUNT_ROUTE)
    api.add_resource(Groups, GROUPS_ROUTE)
    api.add_resource(Group, GROUP_ROUTE, GROUP_POST_ROUTE)
    api.add_resource(StudentToGroup, STUDENT_TO_GROUP_ROUTE)

    api.add_resource(Courses, COURSES_ROUTE)
    api.add_resource(CourseStudents, COURSE_STUDENTS_ROUTE)
    api.add_resource(StudentToCourse, STUDENT_TO_COURSE_ROUTE)

    api.add_resource(Students, STUDENTS_ROUTE)
    api.add_resource(Student, STUDENT_ROUTE, STUDENT_POST_ROUTE)
