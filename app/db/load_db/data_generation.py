import random
import string

from app.configs import GROUPS_AMOUNT, STUDENTS_AMOUNT
from app.db.load_db.data_for_generation import (
    COURSES,
    STUDENT_FIRS_NAMES,
    STUDENT_LAST_NAMES,
)
from app.db.models import Course, Group, Student
from app.db.session import s


def load_db() -> None:
    """This function takes generated students, groups and courses after it
    assign to each student random amount of courses (from 1 to 3) then it
    fills groups by students and add to the database
    """
    students = create_students(STUDENTS_AMOUNT)
    courses = _create_course()

    for student in students:
        student.courses.extend(random.sample(courses, random.randint(1, 3)))

    assigned_students = []

    for group in create_groups(GROUPS_AMOUNT):
        student_amount = random.randint(10, 30)
        if not len(students) > student_amount:
            student_amount = len(students)

        for _ in range(student_amount):
            student = students.pop()
            student.group = group
            assigned_students.append(student)

    s.user_db.add_all(assigned_students)


def create_students(students_amount: int) -> list[Student]:
    """This function generate list with Student instances, equal to
    STUDENTS_AMOUNT"""
    return [
        Student(
            first_name=random.choice(STUDENT_FIRS_NAMES),
            last_name=random.choice(STUDENT_LAST_NAMES),
        )
        for _ in range(students_amount)
    ]


def _create_course() -> list[Course]:
    """This function generate list with Course instances"""
    return [
        Course(name=name, description=desc) for name, desc in COURSES.items()
    ]


def create_groups(groups_amount: int) -> list[Group]:
    """This function generate list with Group instances"""
    return [
        Group(name=group_name)
        for group_name in _generate_group_names(groups_amount)
    ]


def _generate_group_names(groups_amount: int) -> set[str]:
    """This function creates random groups name, while cycle and set guarantee
    that group name will be unique and equal to GROUPS_AMOUNT"""
    groups_name: set = set()
    while len(groups_name) < groups_amount:
        groups_name.add(
            f'{"".join(random.choices(string.ascii_uppercase, k=2))}-'
            f'{"".join(random.choices(string.digits, k=2))}'
        )
    return groups_name
