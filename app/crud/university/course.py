import typing as t

from sqlalchemy import select

from sqlalchemy.orm import (
    selectinload,
    joinedload,
)

from app.api.university.api_models.course import CourseRequest
from app.crud.university.utils import set_value_to_model, get_student_by_ids
from app.db.models import Course

from app.db.session import s


def get_all_courses() -> t.Sequence[Course]:
    """This function returns all courses"""
    statement = select(Course).options(selectinload(Course.students))
    return s.user_db.scalars(statement).all()


def get_course(course_id: int) -> Course | None:
    """This function return course by it id, None if not exist"""
    return s.user_db.get(
        Course, course_id, options=[joinedload(Course.students)]
    )


def add_course(course_data: CourseRequest) -> Course:
    """This function create course and insert it to the database"""
    course = Course(**course_data.model_dump(exclude={"student_ids"}))

    if course_data.student_ids:
        students = get_student_by_ids(course_data.student_ids)
        course.students.extend(students)

    s.user_db.add(course)
    s.user_db.commit()
    s.user_db.refresh(course)
    return course


def update_course(
    course: Course, request_data: CourseRequest, action: str | None
) -> None:
    """This function update course by provided data"""
    course = set_value_to_model(course, request_data, exclude={"students_ids"})
    if request_data.student_ids:
        if action == "append":
            _add_students_to_course(course, request_data.student_ids)
        if action == "remove":
            _remove_students_from_course(course, request_data.student_ids)


def _add_students_to_course(course: Course, student_ids: list[int]) -> None:
    """This function selects students by provided ids, if student already
    persist on course ValueError raised, after check we add students to course
    """
    new_students = get_student_by_ids(student_ids)
    for student in new_students:
        if student in course.students:
            raise ValueError(
                f"Student {student.id} already assigned to {course.name}"
            )
    course.students.extend(new_students)


def _remove_students_from_course(
    course: Course, student_ids: list[int]
) -> None:
    """This function selects students by provided ids, if student don't persist
    on course ValueError raised, after check we remove student from course
    """
    removed_students = get_student_by_ids(student_ids)
    for student in removed_students:
        if student not in course.students:
            raise ValueError(
                f"Student {student.id} don't persist in {course.name}"
            )
        course.students.remove(student)


def overwrite_course(course: Course, request_data: CourseRequest) -> None:
    """This function entirely update the course"""
    course = set_value_to_model(course, request_data, exclude={"students_ids"})
    course.students.clear()
    assert request_data.student_ids
    students = get_student_by_ids(request_data.student_ids)
    course.students.extend(students)


def delete_course(course: Course) -> None:
    """This function delete course from database"""
    s.user_db.delete(course)


def get_course_by_name(course_name: str) -> Course | None:
    """This function return students which related to course"""
    statement = (
        select(Course)
        .options(joinedload(Course.students))
        .where(Course.name == course_name)
    )
    return s.user_db.scalar(statement)
