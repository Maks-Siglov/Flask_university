import sys
import logging

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from app.db.session import s

log = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def transaction(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        s.user_db_transaction = s.user_db.begin()
        assert s.user_db_transaction is not None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            log.exception(f"Error in transaction: {e}")
            if s.user_db_transaction.is_active:
                try:
                    s.user_db_transaction.rollback()
                except Exception:
                    log.exception("Error during transaction rollback")
            raise e
        finally:
            s.user_db.commit()
            s.user_db_transaction = None
        _end_transaction()
        return result

    return wrapper


def _end_transaction() -> None:
    assert s.user_db_transaction
    try:
        s.user_db_transaction.commit()
    except Exception as exc:
        _, _, exc_trace = sys.exc_info()
        try:
            s.user_db_transaction.rollback()
        except Exception:
            log.exception("Error during transaction rollback")

        raise exc.with_traceback(exc_trace)
