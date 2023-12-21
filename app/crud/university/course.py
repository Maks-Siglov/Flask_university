import typing as t

from sqlalchemy import select, not_
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.course import CourseRequest
from app.crud.university.utils import (
    get_student_by_ids,
    set_value_to_model,
)
from app.db.models import Course, Student
from app.db.session import s


def get_all_courses() -> t.Sequence[Course]:
    """This function returns all courses with their students"""
    statement = select(Course).options(selectinload(Course.students))
    return s.user_db.scalars(statement).all()


def get_course(course_id: int) -> Course | None:
    """This function return course with students by it id, None if not exist"""
    return s.user_db.get(
        Course, course_id, options=(joinedload(Course.students),)
    )


def post_course(course_data: CourseRequest) -> Course:
    """This function create course and insert it to the database if student_ids
    provided in request data, it also adds them to the course"""
    course = Course(name=course_data.name, description=course_data.description)

    if course_data.student_ids:
        students = get_student_by_ids(course_data.student_ids)
        course.students.extend(students)

    s.user_db.add(course)
    s.user_db.commit()
    s.user_db.refresh(course)
    return course


def update_course(
    course: Course, request_data: CourseRequest, action: str | None
) -> Course:
    """This function update group by provided data, if student_ids persist in
    request data we add them to the course by default, if action = "remove" we
    remove them"""
    course = set_value_to_model(
        course,
        request_data.model_dump(exclude={"students_ids"}, exclude_none=True),
    )

    student_ids = request_data.student_ids
    if student_ids is not None:
        if action == "remove":
            students = _get_student_by_ids_course(
                student_ids, course_id=course.id, with_course=True
            )
            students = list(set(course.students) - set(students))
            course.students = students
            return course

        students = _get_student_by_ids_course(
            student_ids, course_id=course.id, with_course=False
        )
        course.students.extend(students)

    return course


def put_course(course: Course, request_data: CourseRequest) -> Course:
    """This function entirely update the course by provided request data"""
    course = set_value_to_model(
        course,
        request_data={
            "name": request_data.name,
            "description": request_data.description,
        },
    )
    course.students.clear()
    assert request_data.student_ids
    students = get_student_by_ids(request_data.student_ids)
    course.students.extend(students)

    return course


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


def _get_student_by_ids_course(
    student_ids: list[int], course_id: int, with_course: bool
) -> t.Sequence[Student]:
    """This function return students by provided ids, if with_course set to
    True function return students which assigned to course by course id, else
    students without provided course_id"""
    statement = select(Student).where(Student.id.in_(student_ids))

    if with_course:
        statement.where(Student.courses.any(Course.id == course_id))
    else:
        statement.where(not_(Student.courses.any(Course.id == course_id)))

    students = s.user_db.scalars(statement).all()
    if len(students) != len(student_ids):
        ids = set(student_ids) - {student.id for student in students}
        word = "" if with_course else "don't"
        raise ValueError(
            f"There is no students {ids} which {word} assigned to "
            f"course {course_id}"
        )
    return students
