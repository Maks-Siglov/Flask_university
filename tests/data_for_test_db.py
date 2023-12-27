from app.db.models import Course, Group, Student
from app.db.load_db.data_generation import create_students, create_groups
from app.db.session import s

COURSE_ONE = {"name": "Course 1", "description": "Description 1"}
COURSE_TWO = {"name": "Course 2", "description": "Description 2"}
COURSE_THREE = {"name": "Course 3", "description": "Description 3"}
COURSE_WITHOUT_STUDENT = {"name": "Course 4", "description": "Description 4"}
COURSE_FOR_DELETION = {"name": "Course 5", "description": "Description 5"}

AMOUNT_GROUP_WITHOUT_STUDENT = 5

Group_ONE = {"name": "TT-31"}
GROUT_TWO = {"name": "FF-22"}
GROUP_THREE = {"name": "BA-19"}

AMOUNT_STUDENT_WITHOUT_RELATION = 15

STUDENT_ONE = {"first_name": "John", "last_name": "Doe"}
STUDENT_TWO = {"first_name": "Jane", "last_name": "Willi"}
STUDENT_THREE = {"first_name": "Alice", "last_name": "Smith"}


def load_test_db() -> None:
    course_one = Course(**COURSE_ONE)
    course_two = Course(**COURSE_TWO)
    course_three = Course(**COURSE_THREE)
    course_without_student = Course(**COURSE_WITHOUT_STUDENT)
    course_for_delete = Course(**COURSE_FOR_DELETION)

    group_one = Group(**Group_ONE)
    group_two = Group(**GROUT_TWO)
    group_three = Group(**GROUP_THREE)
    groups_without_students = create_groups(AMOUNT_GROUP_WITHOUT_STUDENT)

    student_one = Student(**STUDENT_ONE)
    student_two = Student(**STUDENT_TWO)
    student_three = Student(**STUDENT_THREE)
    students_without_relations = create_students(
        AMOUNT_STUDENT_WITHOUT_RELATION
    )

    student_one.courses.append(course_one)
    student_one.group = group_one
    student_two.courses.append(course_two)
    student_two.group = group_two
    student_three.courses.append(course_three)
    student_three.group = group_three

    s.user_db.add_all(
        [
            student_one,
            student_two,
            student_three,
            course_without_student,
            course_for_delete,
            *groups_without_students,
            *students_without_relations,
        ]
    )
