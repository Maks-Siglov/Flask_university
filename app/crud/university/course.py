from sqlalchemy import (
    and_,
    delete,
    insert,
    select,
)
from sqlalchemy.orm import joinedload

from app.db.models import (
    Course,
    Student,
    StudentCourseAssociationTable,
)
from app.db.session import s


def course_students(course_name: str) -> list[Student] | None:
    """This query return students which related to course"""
    statement = (
        select(Course)
        .options(joinedload(Course.students))
        .where(Course.name == course_name)
    )
    course = s.user_db.scalar(statement)
    return course.students


def add_student_to_course(student_id: int, course_id: int) -> None:
    """This function take course from database by course_name and insert
    student to it"""
    insert_statement = (
        insert(StudentCourseAssociationTable)
        .values(student_id=student_id, course_id=course_id)
    )

    s.user_db.execute(insert_statement)


def remove_student_from_course(student_id: int, course_id: int) -> None:
    """This function take course from database by course_name then removes
    student from course"""
    delete_statement = (
        delete(StudentCourseAssociationTable)
        .where(and_(
            StudentCourseAssociationTable.student_id == student_id,
            StudentCourseAssociationTable.course_id == course_id
        ))
    )

    s.user_db.execute(delete_statement)


def check_student_assigned_to_course(
        student_id: int, course_id: int,
) -> StudentCourseAssociationTable | None:
    """This function checks if student assigned to course"""
    statement = (
        select(StudentCourseAssociationTable)
        .where(and_(
            StudentCourseAssociationTable.student_id == student_id,
            StudentCourseAssociationTable.course_id == course_id
        ))
    )

    return s.user_db.scalar(statement)
