import typing as t
from pydantic import BaseModel

from app.db.models.base import Base


M = t.TypeVar('M', bound=Base)
T = t.TypeVar('T', bound=BaseModel)


def set_value_to_model(
        model: M, request_data: T, exclude: set[str] | None = None
) -> M:
    """This function set value of request data to model"""
    for field, value in request_data.model_dump(
            exclude=exclude, exclude_none=True
    ).items():
        if hasattr(model, field):
            setattr(model, field, value)
    return model
