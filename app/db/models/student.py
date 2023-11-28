from typing import (
    Any,
    TYPE_CHECKING,
)

from sqlalchemy import ForeignKey
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
    from .course import Course
    from .group import Group


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id', ondelete='RESTRICT'), nullable=True
    )
    group: Mapped['Group'] = relationship(back_populates='students')

    courses: Mapped[list['Course']] = relationship(
        secondary=StudentCourseAssociationTable.__table__,
        back_populates='students'
    )

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        if exclude is None:
            exclude = set()
        student_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        if 'group' not in exclude and self.group:
            student_dict['group'] = self.group.to_dict(exclude={'students'})
        if 'course' not in exclude:
            student_dict['courses'] = [
                course.to_dict(exclude={'students'}) for course in self.courses
            ]

        return student_dict

    def __repr__(self) -> str:
        return (
            f'Student({self.id},'
            f' {self.first_name},'
            f' {self.last_name},'
            f' {self.group},'
            f' {self.courses})'
        )
