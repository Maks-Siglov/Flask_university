import typing as t

from app.api.university.api_models.base import MyBaseModel

if t.TYPE_CHECKING:
    from .student import StudentResponse


class GroupRequest(MyBaseModel):
    name: str | None = None
    student_ids: list[int] | None = None


class GroupResponse(MyBaseModel):
    id: int
    name: str
    students: list["StudentResponse"] | None = None
