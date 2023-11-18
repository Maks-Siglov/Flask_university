

import logging

from sqlalchemy import (
    select,
    func,
    insert,
    delete,
    and_,
)
from sqlalchemy.orm import selectinload

from app.db.session import s
from app.db.models import (
    Group,
    Course,
    Student,
    student_course_association_table,
)

log = logging.getLogger(__name__)


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


def course_students(course_name) -> list[Student]:
    """This query return students which related to course"""
    statement = (
        select(Course)
        .options(selectinload(Course.students))
        .where(Course.name == course_name)
    )
    course = s.user_db.scalar(statement)
    return course.students


def add_student(first_name, last_name) -> None:
    """This function insert student to the database, by provided first and last
    name"""
    statement = insert(Student).values(
        first_name=first_name, last_name=last_name
    )
    s.user_db.execute(statement)


def delete_student(student_id) -> None:
    """At first function deletes student association with courses, after
    delete student itself"""
    delete_association_statement = (
        delete(student_course_association_table)
        .where(student_course_association_table.c.student_id == student_id)
    )
    s.user_db.execute(delete_association_statement)

    delete_statement = delete(Student).where(Student.id == student_id)
    s.user_db.execute(delete_statement)


def add_student_to_course(student_id, course_name) -> None:
    """This function take course from database by course_name and insert
    student to it"""
    course = _take_course_by_name(course_name)

    insert_statement = (
        insert(student_course_association_table)
        .values(student_id=student_id, course_id=course.id)
    )

    s.user_db.execute(insert_statement)


def remove_student_from_course(student_id, course_name) -> None:
    """This function take course from database by course_name then removes
    student from course"""
    course = _take_course_by_name(course_name)

    delete_statement = (
        delete(student_course_association_table)
        .where(and_(
            student_course_association_table.c.student_id == student_id,
            student_course_association_table.c.course_id == course.id
        ))
    )

    s.user_db.execute(delete_statement)


def _take_course_by_name(course_name) -> Course:
    """This function return course by course_name, if it not exists
    ValueError raised"""
    statement = (
        select(Course)
        .where(Course.name == course_name)
    )
    return s.user_db.scalar(statement)
