from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.student_course_association import (
    StudentCourseAssociationTable,
)

if TYPE_CHECKING:
    from app.db.models.course import Course
    from app.db.models.group import Group


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("groups.id", ondelete="SET NULL"), nullable=True
    )
    group: Mapped["Group"] = relationship(back_populates="students")

    courses: Mapped[list["Course"]] = relationship(
        secondary=StudentCourseAssociationTable.__table__,
        back_populates="students",
        join_depth=1,
    )

    def __repr__(self) -> str:
        return (
            f"Student({self.id},"
            f" {self.first_name},"
            f" {self.last_name},"
            f" {self.group},"
            f" {self.courses})"
        )
