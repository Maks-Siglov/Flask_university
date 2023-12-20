import typing as t

from sqlalchemy import select, not_

from app.db.models import Course, Student
from app.db.models.base import Base
from app.db.session import s

M = t.TypeVar("M", bound=Base)


def set_value_to_model(model: M, request_data: dict[str, t.Any]) -> M:
    """This function set value of request data to model fields"""
    for field, value in request_data.items():
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


def get_student_by_ids(student_ids: list[int]) -> t.Sequence[Student]:
    """This function returns students by provided ids"""
    statement = select(Student).where(Student.id.in_(student_ids))
    students = s.user_db.scalars(statement).all()
    _validate_student_ids(students, student_ids)
    return students


def get_student_by_ids_group(
    student_ids: list[int], group_id: int | None = None
) -> t.Sequence[Student]:
    """By default, this function return students by provided ids which not
    assigned to group, but if group_id provided, function return students
    assigned to group"""
    statement = select(Student).where(Student.id.in_(student_ids))

    if group_id is not None:
        statement.where(Student.group_id == group_id)
    else:
        statement.where(Student.group_id.is_(None))

    students = s.user_db.scalars(statement).all()
    _validate_student_ids(students, student_ids)
    return students


def get_student_by_ids_course(
    student_ids: list[int], course_id: int, with_course: bool
) -> t.Sequence[Student]:
    """This function return students by provided ids, if with_course set to
    True function return students which assigned to course by course id, else
    students without provided course_id"""
    statement = select(Student).where(Student.id.in_(student_ids))

    if with_course:
        statement.where(Student.courses.any(Course.id == course_id))
    else:
        statement.where(not_(Student.courses.any(Course.id == course_id)))

    students = s.user_db.scalars(statement).all()
    _validate_student_ids(students, student_ids)
    return students


def _validate_student_ids(
    students: t.Sequence[Student], student_ids: list[int]
) -> None:
    """This function check whether amount of students equal student_ids
    if not ValueError raised"""
    if len(students) != len(student_ids):
        ids = set(student_ids) - {student.id for student in students}
        raise ValueError(f"There is no students with this ids {ids}")
