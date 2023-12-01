from pydantic import BaseModel


class StudentRequest(BaseModel):
    first_name: str
    last_name: str


class GroupRequest(BaseModel):
    name: str


class CourseRequest(BaseModel):
    name: str
    description: str


class StudentGroupRequest(BaseModel):
    student_id: int
    group_id: int


class StudentCourserRequest(BaseModel):
    student_id: int
    course_id: int
