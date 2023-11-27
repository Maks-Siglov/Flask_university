from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class StudentCourseAssociationTable(Base):
    __tablename__ = "student_course_association"

    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id', ondelete='CASCADE'),
        primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey('courses.id', ondelete='CASCADE'),
        primary_key=True
    )
