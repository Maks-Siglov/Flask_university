

from typing import Any

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from app.api.university.routers import (
    CourseStudents,
    SelectGroup,
    Student,
    StudentCourse,
)
from app.configs import (
    APP_DEBUG,
    APP_HOST,
    APP_PORT,
)
from app.db.session import (
    close_dbs,
    pop_session,
    set_session,
)

SELECT_GROUP_ROUTE = '/select_group/<int:student_amount>'
COURSE_STUDENTS_ROUTE = '/course_students/<string:course_name>'
STUDENT_POST_ROUTE = '/student'
STUDENT_DELETE_ROUTE = '/student/<int:student_id>'
STUDENT_TO_COURSE_ROUTE = '/student/<int:student_id>/course/<int:course_id>'


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)
    Swagger(app)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args: Any) -> Any:
        pop_session()
        return args

    @app.teardown_appcontext
    def close_db(args: Any) -> Any:
        close_dbs()
        return args

    api.add_resource(SelectGroup, SELECT_GROUP_ROUTE)
    api.add_resource(CourseStudents, COURSE_STUDENTS_ROUTE)
    api.add_resource(Student, STUDENT_POST_ROUTE, STUDENT_DELETE_ROUTE)
    api.add_resource(StudentCourse, STUDENT_TO_COURSE_ROUTE)

    return app


if __name__ == '__main__':
    assert APP_PORT
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
