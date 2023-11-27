from typing import (
    Any,
    TYPE_CHECKING,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.models.base import Base
from app.db.models.student_course_association import (
    StudentCourseAssociationTable
)

if TYPE_CHECKING:
    from .student import Student


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()

    students: Mapped[list['Student']] = relationship(
        secondary=StudentCourseAssociationTable.__table__,
        back_populates='courses'
    )

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        if exclude is None:
            exclude = set()
        course_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
        if 'students' not in exclude:
            course_dict['students'] = [
                s.to_dict(exclude={'course', 'group'}) for s in self.students
            ]

        return course_dict

    def __repr__(self) -> str:
        return f'Course({self.id}, {self.name}, {self.description})'
