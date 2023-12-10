import typing as t

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.group import GroupRequest
from app.crud.university.utils import (
    get_student_by_ids,
    set_value_to_model,
)
from app.db.models import Group, Student
from app.db.session import s


def get_all_groups() -> t.Sequence[Group]:
    """This function returns all groups"""
    statement = select(Group).options(selectinload(Group.students))
    return s.user_db.scalars(statement).all()


def less_or_equal_students_in_group(students_amount: int) -> t.Sequence[Group]:
    """This query return groups which has less or equal amount of student then
    the specified argument"""
    statement = (
        select(Group)
        .join(Group.students)
        .group_by(Group.id)
        .having(func.count(Group.students) <= students_amount)
    )
    return s.user_db.scalars(statement).all()


def get_group(group_id: int) -> Group | None:
    """This function return group by it id, None if not exist"""
    return s.user_db.get(Group, group_id, options=[joinedload(Group.students)])


def add_group(group_data: GroupRequest) -> Group:
    """This function create group and insert it to the database"""
    group = Group(**group_data.model_dump(exclude={"student_ids"}))

    if group_data.student_ids:
        students = get_student_by_ids(group_data.student_ids)
        _validate_student_group(students, group)
        group.students.extend(students)

    s.user_db.add(group)
    s.user_db.commit()
    s.user_db.refresh(group)
    return group


def update_group(
    group: Group, request_data: GroupRequest, action: str | None
) -> Group:
    """This function updates group by provided data"""
    group = set_value_to_model(group, request_data, exclude={"student_ids"})

    if request_data.student_ids:
        students = get_student_by_ids(request_data.student_ids)
        if action == "remove":
            _remove_students_from_group(group, students)
            return group

        _add_students_to_group(group, students)

    return group


def _add_students_to_group(
        group: Group, students: t.Sequence[Student]
) -> None:
    """This function call validation function, if student already persist in
    group ValueError raised, after check we add students to group
    """
    _validate_student_group(students, group)
    group.students.extend(students)


def _remove_students_from_group(
        group: Group, students: t.Sequence[Student]
) -> None:
    """This function check whether student don't persist in group, if yes
    ValueError raised, after check we remove student from group
    """
    for student in students:
        if student not in group.students:
            raise ValueError(
                f"Student {student.id} don't persist in {group.name}"
            )
        group.students.remove(student)


def put_group(group: Group, request_data: GroupRequest) -> Group:
    """This function overwrites group in the database"""
    group = set_value_to_model(group, request_data, exclude={"student_ids"})
    group.students.clear()
    assert request_data.student_ids
    students = get_student_by_ids(request_data.student_ids)
    _validate_student_group(students, group)
    group.students.extend(students)

    return group


def delete_group(group: Group) -> None:
    """This function delete group from database"""
    s.user_db.delete(group)


def _validate_student_group(
    students: t.Sequence[Student], group: Group
) -> None:
    """This function check whether students assigned to group, if yes
    ValueError raised"""
    for student in students:
        if student.group:
            raise ValueError(
                f"Student {student.id} already belong to {group.name}"
            )
