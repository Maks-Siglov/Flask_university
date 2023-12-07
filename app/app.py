import atexit

import typing as t

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from app.logger import logger_config
from app.init_routers import init_api_routers
from app.configs import (
    API_PREFIX,
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
    api = Api(app, prefix=API_PREFIX)
    Swagger(app)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args: t.Any) -> t.Any:
        pop_session()
        return args

    init_api_routers(api)
    return app


app = create_app()


if __name__ == "__main__":
    atexit.register(close_dbs)
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
