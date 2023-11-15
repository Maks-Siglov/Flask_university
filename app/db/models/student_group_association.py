

from sqlalchemy import (
    Table,
    ForeignKey,
    Column
)

from app.db.models.base import Base

student_group_association_table = Table(
    "student_group_association",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("courses_id", ForeignKey("courses.id"), primary_key=True),
)
