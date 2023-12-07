from app.api.university.api_models.base import (
    MyBaseModel,
    BaseGroup,
    BaseStudent,
)


class GroupRequest(MyBaseModel):
    name: str | None = None
    student_ids: list[int] | None = None


class GroupResponse(BaseGroup):
    students: list[BaseStudent] | None = None
