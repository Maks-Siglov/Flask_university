

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

    api.add_resource(SelectGroup, '/select_group/<int:student_amount>/')
    api.add_resource(CourseStudents, '/course_students/<string:course_name>')
    api.add_resource(Student, '/student/<int:student_id>', '/student/')
    api.add_resource(
        StudentCourse, '/student/<int:student_id>/course/<int:course_id>'
    )

    return app


if __name__ == '__main__':
    assert APP_PORT
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
