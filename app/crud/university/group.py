import typing as t

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.group import GroupRequest
from app.crud.university.utils import (
    get_student_by_ids,
    set_value_to_model,
)
from app.db.models import Group
from app.db.session import s


def get_all_groups() -> t.Sequence[Group]:
    """This function returns all groups with students"""
    statement = select(Group).options(selectinload(Group.students))
    return s.user_db.scalars(statement).all()


def less_or_equal_students_in_group(students_amount: int) -> t.Sequence[Group]:
    """This query return groups which has less or equal amount of student then
    the specified students_amount argument"""
    statement = (
        select(Group)
        .join(Group.students)
        .group_by(Group.id)
        .having(func.count(Group.students) <= students_amount)
    )
    return s.user_db.scalars(statement).all()


def get_group(group_id: int) -> Group | None:
    """This function return group with students by it id, None if not exist"""
    return s.user_db.get(
        Group, group_id, options=(joinedload(Group.students),)
    )


def post_group(group_data: GroupRequest) -> Group:
    """This function create group and insert it to the database if student_ids
    provided in request data, it also adds them to the group"""
    group = Group(**group_data.model_dump(exclude={"student_ids"}))

    if group_data.student_ids:
        students = get_student_by_ids(
            group_data.student_ids, without_group=True
        )
        group.students.extend(students)

    s.user_db.add(group)
    s.user_db.commit()
    s.user_db.refresh(group)
    return group


def update_group(
    group: Group, request_data: GroupRequest, action: str | None
) -> Group:
    """This function update group by provided data, if student_ids persist in
    request data we add them to the group by default, if action = "remove" we
    remove them"""
    group = set_value_to_model(group, request_data, exclude={"student_ids"})

    if request_data.student_ids:
        if action == "remove":
            _remove_students_from_group(group, request_data.student_ids)
            return group

        _add_students_to_group(group, request_data.student_ids)

    return group


def _add_students_to_group(group: Group, student_ids: list[int]) -> None:
    """This function calls validation function, after check we add students to
    the group"""
    students = get_student_by_ids(student_ids, without_group=True)
    group.students.extend(students)


def _remove_students_from_group(group: Group, student_ids: list[int]) -> None:
    """This function check whether student don't persist in group, if yes
    ValueError raised, after check we remove student from group
    """
    students = get_student_by_ids(student_ids, group_id=group.id)
    for student in students:
        group.students.remove(student)


def put_group(group: Group, request_data: GroupRequest) -> Group:
    """This function overwrites group in the database by provided request
    data"""
    group = set_value_to_model(group, request_data, exclude={"student_ids"})
    group.students.clear()
    assert request_data.student_ids
    students = get_student_by_ids(request_data.student_ids, without_group=True)
    group.students.extend(students)

    return group


def delete_group(group: Group) -> None:
    """This function delete group from database"""
    s.user_db.delete(group)
