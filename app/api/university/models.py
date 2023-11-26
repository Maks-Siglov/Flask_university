from pydantic import BaseModel


class StudentRequest(BaseModel):
    first_name: str
    last_name: str


class StudentCourserRequest(BaseModel):
    student_id: int
    course_id: int
