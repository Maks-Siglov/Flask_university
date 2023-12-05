from typing import (
    Any,
    TYPE_CHECKING,
)

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from .student import Student


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(5), unique=True)

    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        if exclude is None:
            exclude = set()
        group_dict = {
            "id": self.id,
            "name": self.name,
        }
        if "students" not in exclude:
            group_dict["students"] = [
                s.to_dict(exclude={"course", "group"}) for s in self.students
            ]

        return group_dict

    def __repr__(self) -> str:
        return f"Group({self.id}, {self.name})"
