from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.student_course_association import (
    StudentToCourse,
)

if TYPE_CHECKING:
    from app.db.models.student import Student


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()

    students: Mapped[list["Student"]] = relationship(
        secondary=StudentToCourse.__table__,
        back_populates="courses",
        join_depth=1,
    )

    def __repr__(self) -> str:
        return f"Course({self.id}, {self.name}, {self.description})"
