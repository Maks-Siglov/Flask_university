from sqlalchemy import (
    and_,
    delete,
    func,
    insert,
    select,
    Sequence,
)
from sqlalchemy.orm import joinedload

from app.api.university.models import StudentRequest
from app.db.models import (
    Course,
    Group,
    Student,
)
from app.db.session import s


def get_student(student_id: int) -> Student | None:
    """This function return student by it id, None if not exist"""
    statement = (
        select(Student)
        .options(joinedload(Student.courses), joinedload(Student.group))
        .where(Student.id == student_id)
    )
    return s.user_db.scalar(statement)


def add_student(student: StudentRequest) -> int:
    """This function insert student to the database"""
    statement = (
        insert(Student)
        .values(**student.model_dump())
        .returning(Student.id)
    )

    return s.user_db.scalar(statement)


def delete_student(student_id: int) -> None:
    """This function delete student from database"""
    delete_statement = delete(Student).where(Student.id == student_id)
    s.user_db.execute(delete_statement)
