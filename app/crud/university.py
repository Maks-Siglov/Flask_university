

from typing import Union

from sqlalchemy import (
    and_,
    delete,
    func,
    insert,
    select,
    Sequence,
    Row
)
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from app.logger import create_logger
from app.api.university.models import StudentRequest
from app.db.models import (
    Course,
    Group,
    Student,
    student_course_association_table,
)
from app.db.session import s

log = create_logger(__name__)


def less_or_equal_students_in_group(
        students_amount: int
) -> Sequence[Group] | None:
    """This query return groups which has less or equal amount of student then
    the specified argument"""
    statement = (
        select(Group)
        .join(Group.students)
        .group_by(Group.id)
        .having(func.count(Group.students) <= students_amount)
    )
    return s.user_db.scalars(statement).all()


def course_students(course_name: str) -> list[Student]:
    """This query return students which related to course"""
    statement = (
        select(Course)
        .options(selectinload(Course.students))
        .where(Course.name == course_name)
    )
    course = s.user_db.scalar(statement)
    return course.students


def get_student(student_id: int) -> Student | None:
    """This function return student by it id, None if not exist"""
    statement = select(Student).where(Student.id == student_id)
    return s.user_db.scalar(statement)


def add_student(student: StudentRequest) -> int:
    """This function insert student to the database"""
    statement = (
        insert(Student)
        .values(student.model_dump())
        .returning(Student.id)
    )

    return s.user_db.execute(statement).first()[0]


def delete_student(student_id: int) -> None:
    """At first function deletes student association with courses, after
    delete student itself"""
    delete_association_statement = (
        delete(student_course_association_table)
        .where(student_course_association_table.c.student_id == student_id)
    )
    s.user_db.execute(delete_association_statement)

    delete_statement = delete(Student).where(Student.id == student_id)
    s.user_db.execute(delete_statement)


def add_student_to_course(student_id: int, course_id: int) -> None:
    """This function take course from database by course_name and insert
    student to it"""
    insert_statement = (
        insert(student_course_association_table)
        .values(student_id=student_id, course_id=course_id)
    )

    s.user_db.execute(insert_statement)


def remove_student_from_course(student_id: int, course_id: int) -> None:
    """This function take course from database by course_name then removes
    student from course"""
    delete_statement = (
        delete(student_course_association_table)
        .where(and_(
            student_course_association_table.c.student_id == student_id,
            student_course_association_table.c.course_id == course_id
        ))
    )

    s.user_db.execute(delete_statement)


def check_student_assigned_to_course(
        student_id: int,
        course_id: int,
) -> Union[Row, None]:
    """This function checks if student assigned to course"""
    statement = _student_to_course_statement(student_id, course_id)
    return s.user_db.scalar(statement)


def get_student_assigned_to_course(
        student_id: int,
        course_id: int,
) -> Union[Row, None]:
    """This function returns student association to course"""
    statement = _student_to_course_statement(student_id, course_id)
    return s.user_db.execute(statement).first()


def _student_to_course_statement(student_id: int, course_id: int,) -> Select:
    return (
        select(student_course_association_table)
        .where(and_(
            student_course_association_table.c.student_id == student_id,
            student_course_association_table.c.course_id == course_id
        ))
    )
