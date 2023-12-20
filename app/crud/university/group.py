import typing as t

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.api.university.api_models.group import GroupRequest
from app.crud.university.utils import (
    get_student_by_ids,
    get_student_by_ids_group,
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
    group = Group(name=group_data.name)

    if group_data.student_ids:
        students = get_student_by_ids_group(group_data.student_ids)
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
    group = set_value_to_model(
        group,
        request_data.model_dump(exclude={"students_ids"}, exclude_none=True),
    )

    student_ids = request_data.student_ids
    if student_ids is not None:
        if action == "remove":
            students = get_student_by_ids_group(student_ids, group_id=group.id)
            students = list(set(group.students) - set(students))
            group.students = students
            return group

        students = get_student_by_ids(student_ids)
        group.students.extend(students)

    return group


def put_group(group: Group, request_data: GroupRequest) -> Group:
    """This function overwrites group in the database by provided request
    data"""
    group = set_value_to_model(group, request_data={"name": request_data.name})
    group.students.clear()
    assert request_data.student_ids
    students = get_student_by_ids_group(request_data.student_ids)
    group.students.extend(students)

    return group


def delete_group(group: Group) -> None:
    """This function delete group from database"""
    s.user_db.delete(group)
