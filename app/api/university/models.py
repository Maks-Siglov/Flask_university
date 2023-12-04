from typing import Union
from pydantic import BaseModel, ConfigDict


class MyBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StudentRequest(MyBaseModel):
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None
    course_ids: list[int] | None = None


class StudentResponse(MyBaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    group: Union['GroupResponse', None] = None
    courses: list['CourseResponse'] | None = None


class StudentResponse2(MyBaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None


class CourseRequest(MyBaseModel):
    name: str | None = None
    description: str | None = None
    student_ids: list[int] | None = None


class CourseResponse(MyBaseModel):
    id: int
    name: str
    description: str
    students: list[StudentResponse2] | None = None


class GroupRequest(MyBaseModel):
    name: str | None = None
    student_ids: list[int] | None = None


class GroupResponse(MyBaseModel):
    id: int
    name: str
    students: list[StudentResponse2] | None = None
