from sqlalchemy import (
    and_,
    delete,
    insert,
    select,
)
from sqlalchemy.orm import (
    selectinload,
    joinedload,
)

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
            selectinload(Course.students)
        )
    )
    return s.user_db.scalars(statement).all()


def course_by_name(course_name: str) -> Course | None:
    """This function return students which related to course"""
    statement = (
        select(Course)
        .options(joinedload(Course.students))
        .where(Course.name == course_name)
    )
    return s.user_db.scalar(statement)


def get_course(course_id: int) -> Course | None:
    """This function return course by it id, None if not exist"""
    return s.user_db.get(
        Course, course_id, options=[joinedload(Course.students)]
    )


def add_course(course: CourseRequest) -> int:
    """This function create course and insert it to the database"""
    statement = (
        insert(Course)
        .values(**course.model_dump())
        .returning(Course.id)
    )
    return s.user_db.scalar(statement)


def update_course(course: Course, data: CourseRequest) -> None:
    """This function update course by provided data"""
    course.name = data.name
    course.description = data.description
    if not data.student_ids:
        return

    students = s.user_db.scalars(
        select(Student)
        .where(Student.id.in_(data.student_ids))
    ).all()
    if len(students) != len(course.students):
        raise ValueError('Invalid student ids')

    course.students.clear()
    course.students.extend(students)


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
