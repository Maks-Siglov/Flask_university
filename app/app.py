

from typing import Any
from flask import Flask
from flask_restful import Api

from app.db.session import (
    set_session,
    pop_sessions,
    close_dbs
)
from app.api.routers import (
    SelectGroup,
    CourseStudents,
    AddStudent,
    DeleteStudent,
    AddStudentToCourse,
    RemoveStudentFromCourse,
)
from app.configs import (
    APP_HOST,
    APP_PORT,
    APP_DEBUG
)


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args: Any) -> Any:
        pop_sessions()
        return args

    @app.teardown_appcontext
    def close_db(args: Any) -> Any:
        close_dbs()
        return args

    api.add_resource(SelectGroup, '/')
    api.add_resource(CourseStudents, '/course_students')
    api.add_resource(AddStudent, '/add_student')
    api.add_resource(DeleteStudent, '/delete_student')
    api.add_resource(AddStudentToCourse, '/add_student_to_course')
    api.add_resource(RemoveStudentFromCourse, '/remove_student_from_course')

    return app


if __name__ == '__main__':
    assert APP_PORT
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
