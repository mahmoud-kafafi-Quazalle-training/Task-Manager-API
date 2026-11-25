from pydantic import BaseModel, ConfigDict
from typing_extensions import TypedDict

from app.domain.task import TaskStatus


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str = ""


class TaskUpdate(TypedDict, total=False):
    __pydantic_config__ = ConfigDict(extra="forbid")

    title: str
    description: str
    status: TaskStatus


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatus


class DeleteTaskResponse(BaseModel):
    message: str
