from sqlalchemy import (
    and_,
    delete,
    func,
    insert,
    select,
    update,
    Sequence,
)
from sqlalchemy.orm import joinedload

from app.api.university.models import GroupRequest
from app.db.models import (
    Group,
    Student,
)
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
    statement = (
        select(Group)
        .options(joinedload(Group.students))
        .where(Group.id == group_id)
    )
    return s.user_db.scalar(statement)


def add_group(group: GroupRequest) -> int:
    """This function create group and insert it to the database"""
    statement = (
        insert(Group)
        .values(**group.model_dump())
        .returning(Group.id)
    )
    return s.user_db.scalar(statement)


def delete_group(group_id: int) -> None:
    """This function delete group from database"""
    delete_statement = (
        delete(Group)
        .where(Group.id == group_id)
    )
    s.user_db.execute(delete_statement)


def add_student_to_group(student_id: int, group_id: int) -> None:
    """This function add student to the grop by updating student group_id"""
    statement = (
        update(Student)
        .where(Student.id == student_id)
        .values({'group_id': group_id})
    )
    s.user_db.execute(statement)


def remove_student_from_group(student_id: int) -> None:
    statement = (
        update(Student)
        .where(Student.id == student_id)
        .values({'group_id': None})
    )
    s.user_db.execute(statement)


def check_student_assigned_to_group(
        student_id: int, group_id: int
) -> Student | None:
    """This function checks if the student persist in group"""
    statement = (
        select(Student)
        .where(and_(
            Student.id == student_id,
            Student.group_id == group_id
        ))
    )
    return s.user_db.scalar(statement)
