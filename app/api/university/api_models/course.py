import typing as t

from app.api.university.api_models.base import MyBaseModel

if t.TYPE_CHECKING:
    from app.api.university.api_models.student import StudentResponse


class CourseRequest(MyBaseModel):
    name: str | None = None
    description: str | None = None
    student_ids: list[int] | None = None


class CourseResponse(MyBaseModel):
    id: int
    name: str
    description: str
    students: t.Optional[list["StudentResponse"]] = None
