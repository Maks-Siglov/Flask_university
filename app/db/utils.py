import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

from app.db.models.base import Base
from app.db.session import s

log = logging.getLogger(__name__)


def create_database(db_url: str, db_name: str) -> None:
    try:
        with create_engine(
            db_url, isolation_level="AUTOCOMMIT"
        ).begin() as connect:
            connect.execute(text(f"CREATE DATABASE {db_name}"))
            log.info(f"Database {db_name} created")
    except ProgrammingError:
        log.info(f"Database {db_name} already exist")


def drop_database(db_url: str, db_name: str) -> None:
    try:
        with create_engine(
            db_url, isolation_level="AUTOCOMMIT"
        ).begin() as connect:
            connect.execute(text(f"DROP DATABASE {db_name} WITH(FORCE);"))
            log.info(f"Database {db_name} dropped")
    except ProgrammingError:
        log.info(f"Database {db_name} don't exist")


def init_database(db_url: str, db_name: str) -> None:
    import alembic.command
    import alembic.config

    alembic_config = alembic.config.Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", f"{db_url}/{db_name}")
    alembic.command.upgrade(alembic_config, "head")
    log.info(f"Alembic upgrade db: {db_url}/{db_name}")


def create_table() -> None:
    Base.metadata.create_all(s.user_db.get_bind())


def drop_table() -> None:
    Base.metadata.drop_all(s.user_db.get_bind())
