from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
