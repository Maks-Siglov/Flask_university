from typing import Any

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from app.logger import logger_config
from app.init_routers import init_api_routers
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
    logger_config()
    app = Flask(__name__)
    api = Api(app)
    init_api_routers(api)
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

    return app


if __name__ == '__main__':
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
