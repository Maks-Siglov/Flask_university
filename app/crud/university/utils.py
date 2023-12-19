import typing as t

from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.sql.expression import ColumnElement


from app.db.models import Course, Student
from app.db.models.base import Base
from app.db.session import s

M = t.TypeVar("M", bound=Base)
T = t.TypeVar("T", bound=BaseModel)


def set_value_to_model(
    model: M, request_data: T, exclude: set[str] | None = None
) -> M:
    """This function set value of request data to model fields"""
    for field, value in request_data.model_dump(
        exclude=exclude, exclude_none=True
    ).items():
        if hasattr(model, field):
            setattr(model, field, value)
    return model


def get_course_by_ids(course_ids: list[int]) -> t.Sequence[Course]:
    """This functions returns courses by provided ids, if there is no some id
    ValueError raised"""
    statement = select(Course).where(Course.id.in_(course_ids))
    courses = s.user_db.scalars(statement).all()
    if len(courses) != len(course_ids):
        ids = set(course_ids) - {course.id for course in courses}
        raise ValueError(f"There is no courses with this ids {ids}")
    return courses


def get_student_by_ids(
    student_ids: list[int],
    without_group: bool | None = None,
    group_id: int | None = None,
) -> t.Sequence[Student]:
    """
    This function returns students by provided ids if without_group = True,
    we take only students that not have a group, if group_id passed we take
    students which assigned to the group if amount of students don't equal
    student_ids ValueError raised
    """
    where_statement: ColumnElement = Student.id.in_(student_ids)
    if without_group:
        where_statement = and_(
            Student.id.in_(student_ids), Student.group_id.is_(None)
        )
    if group_id:
        where_statement = and_(
            Student.id.in_(student_ids), Student.group_id == group_id
        )
    statement = select(Student).where(where_statement)
    students = s.user_db.scalars(statement).all()

    if len(students) != len(student_ids):
        ids = set(student_ids) - {student.id for student in students}
        raise ValueError(f"There is no students with this ids {ids}")
    return students
