import typing as t

from app.api.university.api_models.base import MyBaseModel

if t.TYPE_CHECKING:
    from .group import GroupResponse
    from .course import CourseResponse


class StudentRequest(MyBaseModel):
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None
    course_ids: list[int] | None = None


class StudentResponse(MyBaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    group: t.Optional["GroupResponse"] = None
    courses: list["CourseResponse"] | None = None
