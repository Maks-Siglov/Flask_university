from pydantic import BaseModel, ConfigDict


class MyBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def check_not_none_field(self):
        if any(value is None for value in self.model_dump().values()):
            raise ValueError("All fields must be provided")


class BaseStudent(MyBaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None


class BaseCourse(MyBaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None


class BaseGroup(MyBaseModel):
    id: int | None = None
    name: str | None = None
