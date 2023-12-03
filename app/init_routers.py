from flask_restful import Api

from app.api.university.endpoints.student import (
    StudentsApi,
    StudentApi
)
from app.api.university.endpoints.group import (
    GroupStudentAmountApi,
    StudentToGroupApi,
    GroupApi,
    GroupsApi,
)
from app.api.university.endpoints.course import (
    CoursesApi,
    CourseApi,
)


GROUP_STUDENTS_AMOUNT_ROUTE = '/group_students_amount/<int:student_amount>'
GROUPS_ROUTE = '/groups'
GROUP_ROUTE = '/group/<int:group_id>'
GROUP_POST_ROUTE = '/group'
STUDENT_TO_GROUP_ROUTE = '/student_to_group'

STUDENTS_ROUTE = '/students'
STUDENT_POST_ROUTE = '/student'
STUDENT_ROUTE = '/student/<int:student_id>'

COURSES_ROUTE = '/courses'
COURSE_POST_ROUTE = '/course'
COURSE_ROUTE = '/course/<int:course_id>'


def init_api_routers(api: Api):
    api.add_resource(GroupStudentAmountApi, GROUP_STUDENTS_AMOUNT_ROUTE)
    api.add_resource(GroupsApi, GROUPS_ROUTE)
    api.add_resource(GroupApi, GROUP_ROUTE, GROUP_POST_ROUTE)
    api.add_resource(StudentToGroupApi, STUDENT_TO_GROUP_ROUTE)

    api.add_resource(CoursesApi, COURSES_ROUTE)
    api.add_resource(CourseApi, COURSE_ROUTE, COURSE_POST_ROUTE)

    api.add_resource(StudentsApi, STUDENTS_ROUTE)
    api.add_resource(StudentApi, STUDENT_ROUTE, STUDENT_POST_ROUTE)
