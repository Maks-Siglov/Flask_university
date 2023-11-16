

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.models.base import Base
from app.db.models.student_group_association import (
    student_group_association_table
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
        secondary=student_group_association_table, back_populates='students'
    )

    def __repr__(self):
        return f'Student({self.id}, {self.first_name}, {self.last_name})'
