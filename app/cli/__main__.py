

import click

from app.db.utils import (
    create_database,
    drop_database,
    create_table,
    init_database
)
from app.cofigs import (
    DB_NAME,
    BASE_URL,
    POSTGRESS_DB,
)


@click.command()
@click.option('--db_name', default=DB_NAME, help='Name of the database')
@click.option('--create', is_flag=True, help='Create database')
@click.option('--drop', is_flag=True, help='Drop database')
@click.option('--recreate', is_flag=True, help='Recreate database')
@click.option('--init', is_flag=True, help='Execute alembic revision')
def db(
    db_name: str,
    create: bool,
    drop: bool,
    recreate: bool,
    init: bool,
) -> None:
    base_superuser_url = f'{BASE_URL}/{POSTGRESS_DB}'

    if drop:
        drop_database(base_superuser_url, db_name)

    if create:
        create_database(base_superuser_url, db_name)

    if recreate:
        drop_database(base_superuser_url, db_name)
        create_database(base_superuser_url, db_name)

    if init:
        init_database(BASE_URL, db_name)


if __name__ == '__main__':
    db()
