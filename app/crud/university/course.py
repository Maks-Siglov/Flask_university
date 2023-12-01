from sqlalchemy import (
    and_,
    update,
    delete,
    insert,
    select,
)
from sqlalchemy.orm import joinedload

from app.api.university.models import CourseRequest
from app.db.models import (
    Course,
    Student,
    StudentCourseAssociationTable,
)
from app.db.session import s


def get_all_courses() -> list[Course]:
    """This function returns all courses"""
    statement = (
        select(Course).options(
            joinedload(Course.students)
        )
    )
    return s.user_db.scalars(statement).unique().all()


def course_students(course_name: str) -> list[Student] | None:
    """This function return students which related to course"""
    statement = (
        select(Course)
        .options(joinedload(Course.students))
        .where(Course.name == course_name)
    )
    course = s.user_db.scalar(statement)
    return course.students


def get_course(course_id: int) -> Course | None:
    """This function return course by it id, None if not exist"""
    statement = (
        select(Course)
        .options(joinedload(Course.students))
        .where(Course.id == course_id)
    )
    return s.user_db.scalar(statement)


def add_course(course: CourseRequest) -> int:
    """This function create course and insert it to the database"""
    statement = (
        insert(Course)
        .values(**course.model_dump())
        .returning(Course.id)
    )
    return s.user_db.scalar(statement)


def update_course(course_id: int, data: dict[str, str]) -> None:
    """This function update course by provided data"""
    statement = (
        update(Course)
        .where(Course.id == course_id)
        .values(data)
    )
    s.user_db.execute(statement)


def delete_course(course_id: int) -> None:
    """This function delete course from database"""
    delete_statement = (
        delete(Course)
        .where(Course.id == course_id)
    )
    s.user_db.execute(delete_statement)


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
