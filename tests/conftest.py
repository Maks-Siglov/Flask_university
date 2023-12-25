import pytest

from app.app import create_app
from app.db.session import get_sync_pool, s
from app.configs import (
    BASE_URL,
    DB_NAME,
    POSTGRESS_DB,
)
from app.db.session import (
    close_dbs,
    pop_session,
    set_session,
)
from app.db.utils import (
    create_database,
    create_table,
    drop_database,
)
from tests.data_for_test_db import load_test_db

BASE_SUPERUSER_URL = f"{BASE_URL}/{POSTGRESS_DB}"


@pytest.fixture(scope="session")
def app():
    yield create_app()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session", autouse=True)
def db_set_session() -> None:
    current_pool = get_sync_pool(f"{BASE_URL}/{DB_NAME}", {})
    s.user_db = current_pool.maker()
    s.user_db.connection(execution_options={"isolation_level": "SERIALIZABLE"})
    yield
    try:
        s.user_db.commit()
    finally:
        s.user_db.close()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    create_database(BASE_SUPERUSER_URL, DB_NAME)
    set_session()
    create_table()
    load_test_db()
    pop_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        close_dbs()
    finally:
        print("\nClose DB")

    try:
        drop_database(BASE_SUPERUSER_URL, DB_NAME)
    finally:
        print(f"DROP DB {DB_NAME}")
