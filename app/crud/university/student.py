import typing as t

from sqlalchemy import select, not_
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.student import StudentRequest
from app.crud.university.group import get_group
from app.crud.university.utils import (
    get_course_by_ids,
    set_value_to_model,
)
from app.db.models import Student, Course
from app.db.session import s


def get_all_students() -> t.Sequence[Student]:
    """This function returns all students with group and courses"""
    statement = select(Student).options(
        joinedload(Student.group), selectinload(Student.courses)
    )
    return s.user_db.scalars(statement).all()


def get_student(student_id: int) -> Student | None:
    """This function return student with courses by it id, None if not exist"""
    return s.user_db.get(
        Student, student_id, options=(joinedload(Student.courses),)
    )


def get_student_by_name(student_name: str) -> Student | None:
    """This function return student by provided first name"""
    return s.user_db.scalar(
        select(Student).where(Student.first_name == student_name)
    )


def post_student(student_data: StudentRequest) -> Student:
    """This function add student to the database, if course_ids or group_id
    persist in request data it adds them to student"""
    student = Student(
        first_name=student_data.first_name,
        last_name=student_data.last_name,
    )

    s.user_db.add(student)
    if student_data.course_ids:
        courses = get_course_by_ids(student_data.course_ids)
        student.courses.extend(courses)

    if student_data.group_id:
        group = get_group(student_data.group_id)
        if not group:
            s.user_db.delete(student)
            raise ValueError(f"Group {student_data.group_id} don't exist")
        student.group = group

    s.user_db.commit()
    s.user_db.refresh(student)
    return student


def update_student(
    student: Student, request_data: StudentRequest, action: str | None
) -> Student:
    """This function update student by provided data, if course_ids or group_id
    persist in request data we add them to the student by default, if action =
    "remove" we remove them"""
    student = set_value_to_model(
        student,
        request_data.model_dump(
            exclude={"courses_ids", "group_id"}, exclude_none=True
        ),
    )
    if action == "remove":
        _update_student_with_remove(student, request_data)
        return student

    if request_data.course_ids is not None:
        courses = _get_course_by_ids_student(
            request_data.course_ids, student_id=student.id, with_student=False
        )
        student.courses.extend(courses)

    group_id = request_data.group_id
    if group_id:
        if student.group is not None:
            raise ValueError(
                f"Student {student.id} already assigned to {student.group}"
            )
        group = get_group(group_id)
        if not group:
            raise ValueError(f"Group {group_id} don't exist")
        student.group = group

    return student


def _update_student_with_remove(
    student: Student, request_data: StudentRequest
) -> None:
    """This function remove group and courses by provided ids in request data
    we check group and courses ids if student's group and courses ids not the
    same as provided id, ValueError raised, after checking we add courses and
    group to the student"""
    group_id = request_data.group_id
    if group_id:
        if not student.group_id == group_id:
            raise ValueError(f"Student {student.id} not in group {group_id}")
        student.group_id = None

    if request_data.course_ids is not None:
        courses = _get_course_by_ids_student(
            request_data.course_ids, student_id=student.id, with_student=True
        )
        for course in courses:
            student.courses.remove(course)


def put_student(student: Student, request_data: StudentRequest) -> Student:
    """This function entirely change the student in the database"""
    student = set_value_to_model(
        student,
        request_data={
            "first_name": request_data.first_name,
            "last_name": request_data.last_name,
        },
    )
    student.courses.clear()
    assert request_data.course_ids
    courses = get_course_by_ids(request_data.course_ids)
    student.courses.extend(courses)

    assert request_data.group_id
    group = get_group(request_data.group_id)
    if not group:
        raise ValueError(f"Group {request_data.group_id} don't exist")
    student.group = group

    return student


def delete_student(student: Student) -> None:
    """This function delete student from database"""
    s.user_db.delete(student)


def _get_course_by_ids_student(course_ids, student_id, with_student):
    """This function return courses by provided ids, if with_student set to
    True function return students which assigned to student by student_id, else
    students without provided student_id"""
    statement = select(Course).where(Course.id.in_(course_ids))
    if with_student:
        statement.where(Course.students.any(Student.id == student_id))
    elif not with_student:
        statement.where(not_(Course.students.any(Student.id == student_id)))
    courses = s.user_db.scalars(statement).all()
    if len(courses) != len(course_ids):
        ids = set(course_ids) - {course.id for course in courses}
        word = "" if with_student else "don't"
        raise ValueError(
            f"There is no courses {ids} which {word} assigned "
            f"student {student_id}"
        )
    return courses
