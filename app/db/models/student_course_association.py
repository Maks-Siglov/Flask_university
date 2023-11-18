

from sqlalchemy import (
    Table,
    ForeignKey,
    Column
)

from app.db.models.base import Base

student_course_association_table = Table(
    "student_course_association",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)
