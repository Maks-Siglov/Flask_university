

from typing import Any
from dataclasses import (
    dataclass,
    asdict
)


@dataclass
class StudentRequest:
    first_name: str
    last_name: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if not all(isinstance(item, str) for item in data.values()):
            raise TypeError
        return data
