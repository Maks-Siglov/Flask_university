

import pytest

from app.app import create_app
from app.db.load_db.data_generation import load_db
from app.db.utils import (
    create_database,
    create_table,
    drop_database
)
from app.db.session import (
    set_session,
    pop_session,
    close_dbs,
)
from app.configs import (
    BASE_URL,
    POSTGRESS_DB,
    DB_NAME,
)

BASE_SUPERUSER_URL = f'{BASE_URL}/{POSTGRESS_DB}'


@pytest.fixture(scope='session')
def app():
    app = create_app()
    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    create_database(BASE_SUPERUSER_URL, DB_NAME)
    set_session()
    create_table()
    load_db()
    pop_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        close_dbs()
    finally:
        print('\nClose DB')

    try:
        drop_database(BASE_SUPERUSER_URL, DB_NAME)
    finally:
        print(f'DROP DB {DB_NAME}')
