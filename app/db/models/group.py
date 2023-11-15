

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(5), unique=True)

    def __repr__(self):
        return f'Group({self.id}, {self.name})'
