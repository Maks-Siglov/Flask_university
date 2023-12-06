import typing as t

from app.api.university.api_models.base import MyBaseModel

if t.TYPE_CHECKING:
    from app.api.university.api_models.student import StudentResponse


class GroupRequest(MyBaseModel):
    name: str | None = None
    student_ids: list[int] | None = None


class GroupResponse(MyBaseModel):
    id: int
    name: str
    students: t.Optional[list["StudentResponse"]] = None
