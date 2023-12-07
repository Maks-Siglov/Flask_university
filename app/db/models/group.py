from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.student import Student


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(5), unique=True)

    students: Mapped[list["Student"]] = relationship(
        back_populates="group", join_depth=1
    )

    def __repr__(self) -> str:
        return f"Group({self.id}, {self.name})"
