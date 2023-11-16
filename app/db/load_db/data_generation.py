

import random
import string

from app.db.session import s
from app.db.models import (
    Group,
    Student,
    Course,
)
from app.db.load_db.data_for_generation import (
    STUDENT_FIRS_NAMES,
    STUDENT_LAST_NAMES,
    COURSES,
)
from app.configs import (
    GROUPS_AMOUNT,
    STUDENTS_AMOUNT,
)


def load_db():
    """This function takes generated students, groups and courses after it
    assign to each student random amount of courses (from 1 to 3) then it
    fills groups by students and add to the database
    """
    students = _create_students()
    courses = _create_course()

    for student in students:
        student.courses.extend(
            random.sample(courses, random.randint(1, 3))
        )

    assigned_students = []

    for group in _create_groups():
        student_amount = random.randint(10, 30)
        if not len(students) > student_amount:
            student_amount = len(students)

        for _ in range(student_amount):
            student = students.pop()
            student.group = group
            assigned_students.append(student)
        print('fff', group, len(group.students))

    s.user_db.add_all(assigned_students)


def _create_students() -> list[Student]:
    """This function generate list with Student instances, equal to
    STUDENTS_AMOUNT"""
    return [
        Student(
            first_name=random.choice(STUDENT_FIRS_NAMES),
            last_name=random.choice(STUDENT_LAST_NAMES),
        ) for _ in range(STUDENTS_AMOUNT)
    ]


def _create_course() -> list[Course]:
    """This function generate list with Course instances"""
    return [
        Course(name=name, description=desc) for name, desc in COURSES.items()
    ]


def _create_groups() -> list[Group]:
    """This function generate list with Group instances"""
    return [Group(name=group_name) for group_name in _generate_group_names()]


def _generate_group_names() -> set[str]:
    """This function creates random groups name, while cycle and set guarantee
    that group name will be unique and equal to GROUPS_AMOUNT"""
    groups_name = set()
    while len(groups_name) < GROUPS_AMOUNT:
        groups_name.add(
            f'{"".join(random.choices(string.ascii_uppercase, k=2))}-'
            f'{"".join(random.choices(string.digits, k=2))}'
        )
    return groups_name
