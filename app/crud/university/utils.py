import typing as t

from pydantic import BaseModel
from sqlalchemy import select

from app.db.models import Course, Student
from app.db.models.base import Base
from app.db.session import s

M = t.TypeVar("M", bound=Base)
T = t.TypeVar("T", bound=BaseModel)


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


def get_course_by_ids(course_ids: list[int]) -> t.Sequence[Course]:
    """This functions returns courses by provided ids"""
    statement = select(Course).where(Course.id.in_(course_ids))
    courses = s.user_db.scalars(statement).all()
    if len(courses) != len(course_ids):
        raise ValueError("There is no courses with this ids")
    return courses


def get_student_by_ids(student_ids: list[int]) -> t.Sequence[Student]:
    """This function returns students by provided ids"""
    statement = select(Student).where(Student.id.in_(student_ids))
    students = s.user_db.scalars(statement).all()
    if len(students) != len(student_ids):
        raise ValueError("There is no students with this ids")
    return students
