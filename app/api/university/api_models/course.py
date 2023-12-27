from app.api.university.api_models.base import (
    BaseCourse,
    BaseStudent,
    MyBaseModel,
)


class CourseRequest(MyBaseModel):
    name: str | None = None
    description: str | None = None
    student_ids: list[int] | None = None


class CourseResponse(BaseCourse):
    students: list[BaseStudent] | None = None
