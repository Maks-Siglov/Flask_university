from app.api.university.api_models.base import (
    MyBaseModel,
    BaseStudent,
    BaseCourse,
    BaseGroup,
)


class StudentRequest(MyBaseModel):
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None
    course_ids: list[int] | None = None


class StudentResponse(BaseStudent):
    group: BaseGroup | None = None
    courses: list[BaseCourse] | None = None
