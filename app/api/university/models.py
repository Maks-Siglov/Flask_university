from pydantic import BaseModel, Field


class StudentRequest(BaseModel):
    first_name: str = Field(default='Default first name')
    last_name: str = Field(default='Default last name')


class GroupRequest(BaseModel):
    name: str


class CourseRequest(BaseModel):
    name: str = Field(default='Default name')
    description: str = Field(default='Default description')
    student_ids: list[int] | None = None


class StudentGroupRequest(BaseModel):
    student_id: int
    group_id: int


class StudentCourserRequest(BaseModel):
    student_id: int
    course_id: int
