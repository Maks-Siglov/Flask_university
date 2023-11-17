

from typing import Any
from flask import Flask
from flask_restful import Api

from app.db.session import (
    set_session,
    pop_sessions,
    close_dbs
)
from app.api.routers import SelectGroup
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

    return app


if __name__ == '__main__':
    assert APP_PORT
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
