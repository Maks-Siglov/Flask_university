
from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.models.base import Base
from app.db.models.student_course_association import (
    student_course_association_table
)

if TYPE_CHECKING:
    from .student import Student


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()

    students: Mapped[list['Student']] = relationship(
        secondary=student_course_association_table, back_populates='courses'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

    def __repr__(self):
        return f'Course({self.id}, {self.name}, {self.description})'
