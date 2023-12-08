import typing as t

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.student import StudentRequest
from app.crud.university.group import get_group
from app.crud.university.utils import (
    get_course_by_ids,
    set_value_to_model,
)
from app.db.models import Student
from app.db.session import s


def get_all_students() -> t.Sequence[Student]:
    """This function returns all students"""
    statement = select(Student).options(
        joinedload(Student.group), selectinload(Student.courses)
    )
    return s.user_db.scalars(statement).all()


def get_student(student_id: int) -> Student | None:
    """This function return student by it id, None if not exist"""
    return s.user_db.get(
        Student, student_id, options=[joinedload(Student.courses)]
    )


def add_student(student_data: StudentRequest) -> Student:
    """This function insert student to the database"""
    student = Student(
        **student_data.model_dump(exclude={"course_ids", "group_id"})
    )
    if student_data.course_ids:
        courses = get_course_by_ids(student_data.course_ids)
        student.courses.extend(courses)

    if student_data.group_id:
        group = get_group(student_data.group_id)
        assert group
        student.group_id = group.id

    s.user_db.add(student)
    s.user_db.commit()
    s.user_db.refresh(student)
    return student


def update_student(
    student: Student, request_data: StudentRequest, action: str | None
) -> Student:
    """This function update student by provided data"""
    student = set_value_to_model(
        student, request_data, exclude={"group_id", "course_ids"}
    )

    if request_data.group_id:
        _change_student_group(student, request_data.group_id, action)

    if request_data.course_ids:
        _update_student_courses(student, request_data.course_ids, action)

    return student


def _change_student_group(
    student: Student, group_id: int, action: str | None
) -> None:
    if action == "append":
        if student.group is not None:
            raise ValueError(
                f"Student {student.id} already assigned to {student.group}"
            )
        student.group = get_group(group_id)

    if action == "remove":
        if not student.group_id == group_id:
            raise ValueError(f"Student {student.id} not in group {group_id}")
        student.group_id = None


def _update_student_courses(
    student: Student, course_ids: list[int], action: str | None
) -> None:
    courses = get_course_by_ids(course_ids)
    if action == "append":
        for course in courses:
            if course in student.courses:
                raise ValueError(
                    f"Student {student.id} already assigned to {course}"
                )
        student.courses.extend(courses)

    if action == "remove":
        for course in courses:
            if course not in student.courses:
                raise ValueError(
                    f"Student {student.id} don't assign to {course}"
                )
            student.courses.remove(course)


def put_student(student: Student, request_data: StudentRequest) -> Student:
    """This function entirely change the student in the database"""
    student = set_value_to_model(
        student, request_data, exclude={"group_id", "course_ids"}
    )
    student.courses.clear()
    assert request_data.course_ids
    courses = get_course_by_ids(request_data.course_ids)
    student.courses.extend(courses)

    assert request_data.group_id
    new_group = get_group(request_data.group_id)
    assert new_group
    student.group = new_group

    return student


def delete_student(student: Student) -> None:
    """This function delete student from database"""
    s.user_db.delete(student)
