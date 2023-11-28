from app.db.session import s
from app.db.models import (
    Student,
    Course,
    Group,
)

COURSE_ONE = {
    'id': 1, 'name': 'course_one_student', 'description': 'Description 1'
}
COURSE_TWO = {
    'id': 2, 'name': 'course_two_student', 'description': 'Description 2'
}
COURSE_WITHOUT_STUDENT = {
    'id': 3, 'name': 'course_without_student', 'description': 'Description 3'
}


Group_ONE = {'id': 1, 'name': 'TT-31'}
GROUT_TWO = {'id': 2, 'name': 'FF-22'}
GROUT_WITHOUT_STUDENT = {'id': 3, 'name': 'AG-73'}


STUDENT_ONE = {
    'first_name': 'John', 'last_name': 'Doe'
}
STUDENT_TWO = {
    'first_name': 'Jane', 'last_name': 'Doe'
}
STUDENT_THREE = {
    'first_name': 'Olivia', 'last_name': 'Thomas'
}
STUDENT_WITHOUT_COURSE = {
  'first_name': 'Alice', 'last_name': 'Wonderland'
}


def load_test_db():
    course_one = Course(**COURSE_ONE)
    course_two = Course(**COURSE_TWO)
    course_without_student = Course(**COURSE_WITHOUT_STUDENT)

    group_one = Group(**Group_ONE)
    group_two = Group(**GROUT_TWO)
    group_without_students = Group(**GROUT_WITHOUT_STUDENT)

    student_one = Student(**STUDENT_ONE)
    student_two = Student(**STUDENT_TWO)
    student_three = Student(**STUDENT_THREE)
    student_without_course = Student(**STUDENT_WITHOUT_COURSE)

    student_one.courses.append(course_one)
    student_one.group = group_one
    student_two.courses.append(course_two)
    student_two.group = group_two
    student_three.courses.append(course_two)

    s.user_db.add_all(
        [
            student_one, student_two, student_without_course,
            course_without_student, student_three, group_without_students
        ]
    )



