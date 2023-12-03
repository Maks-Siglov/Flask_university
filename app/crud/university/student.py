from sqlalchemy import (
    delete,
    insert,
    select,
)
from sqlalchemy.orm import (
    joinedload,
    selectinload,
)
from sqlalchemy import Sequence


from app.api.university.models import StudentRequest
from app.db.models import Student
from app.db.session import s


def get_all_students() -> list[Student]:
    """This function returns all students"""
    statement = (
        select(Student).options(
            joinedload(Student.group),
            selectinload(Student.courses)
        )
    )
    return s.user_db.scalars(statement).all()


def get_student_by_ids(student_ids: list[int]) -> Sequence[Student]:
    """This function returns students by provided ids"""
    students = s.user_db.scalars(
        select(Student).where(Student.id.in_(student_ids))
    ).all()
    return students


def get_student(student_id: int) -> Student | None:
    """This function return student by it id, None if not exist"""
    return s.user_db.get(
        Student, student_id, options=[joinedload(Student.courses)]
    )


def add_student(student: StudentRequest) -> int:
    """This function insert student to the database"""
    statement = (
        insert(Student)
        .values(**student.model_dump())
        .returning(Student.id)
    )

    return s.user_db.scalar(statement)


def update_student(student: Student, data: StudentRequest) -> None:
    """This function update student by provided data"""
    student.first_name = data.first_name
    student.last_name = data.last_name


def delete_student(student_id: int) -> None:
    """This function delete student from database"""
    delete_statement = delete(Student).where(Student.id == student_id)
    s.user_db.execute(delete_statement)
