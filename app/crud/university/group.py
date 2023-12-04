from sqlalchemy import (
    func,
    select,
    Sequence,
)
from sqlalchemy.orm import joinedload

from app.crud.university.utils import set_value_to_model
from app.crud.university.student import get_student_by_ids
from app.api.university.models import GroupRequest
from app.db.models import Group
from app.db.session import s


def get_all_groups() -> list[Group]:
    """This function returns all groups"""
    statement = (
        select(Group).options(
            joinedload(Group.students)
        )
    )
    return s.user_db.scalars(statement).unique().all()


def less_or_equal_students_in_group(
        students_amount: int
) -> Sequence[Group]:
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
    return s.user_db.get(
        Group, group_id, options=[joinedload(Group.students)]
    )


def get_group_by_name(group_name: str) -> Group | None:
    statement = (
        select(Group)
        .where(Group.name == group_name)
    )
    return s.user_db.scalar(statement)


def add_group(group_data: GroupRequest) -> Group:
    """This function create group and insert it to the database"""
    group = Group(**group_data.model_dump(exclude={'student_ids'}))

    if group_data.student_ids:
        students = get_student_by_ids(group_data.student_ids)
        for student in students:
            if student.group:
                raise ValueError(
                    f'Student {student.id} already belong to {student.group}'
                )
        group.students.extend(students)

    s.user_db.add(group)
    s.user_db.commit()
    s.user_db.refresh(group)
    return group


def update_group(
        group: Group, request_data: GroupRequest, append: bool, remove: bool
) -> None:
    """This function updates group by provided data"""
    group = set_value_to_model(group, request_data, exclude={'student_ids'})
    if request_data.student_ids:
        if append:
            _add_students_to_group(group, request_data.student_ids)
        if remove:
            _remove_students_from_group(group, request_data.student_ids)


def _add_students_to_group(
        group: Group, student_ids: list[int]
) -> None:
    """This function selects students by provided ids, if student already
    persist in group ValueError raised, after check we add students to group
    """
    new_students = get_student_by_ids(student_ids)
    for student in new_students:
        if student.group:
            raise ValueError(
                f'Student {student.id} already belong to {group.name}'
            )
    group.students.extend(new_students)


def _remove_students_from_group(
        group: Group, student_ids: list[int]
) -> None:
    """This function selects students by provided ids, if student don't persist
     in group ValueError raised, after check we remove student from group
    """
    removed_students = get_student_by_ids(student_ids)
    for student in removed_students:
        if student not in group.students:
            raise ValueError(
                f"Student {student.id} don't persist in {group.name}"
            )
        group.students.remove(student)


def delete_group(group: Group) -> None:
    """This function delete group from database"""
    s.user_db.delete(group)
