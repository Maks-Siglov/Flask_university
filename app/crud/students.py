

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.session import s
from app.db.models import (
    Group,
    Course,
)


def less_or_equal_students_in_group(students_amount) -> list[Group] | None:
    """This query return groups which has less or equal amount of student then
    the specified argument"""
    statement = (
        select(Group)
        .join(Group.students)
        .group_by(Group.id)
        .having(func.count(Group.students) <= students_amount)
    )
    return s.user_db.scalars(statement).all()


def course_students(course_name):
    """This query return students which related to course"""
    statement = (
        select(Course)
        .options(selectinload(Course.students))
        .where(Course.name == course_name)
    )
    course = s.user_db.scalar(statement)
    return course.students
