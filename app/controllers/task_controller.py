from typing import Annotated

from fastapi import Depends

from app.dependencies import get_task_service
from app.domain.task import Task
from app.schemas.task_schema import DeleteTaskResponse, TaskCreate, TaskUpdate
from app.services.task_service import TaskService

TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


def create_task(data: TaskCreate, service: TaskServiceDependency) -> Task:
    return service.create_task(data.title, data.description)


def list_tasks(service: TaskServiceDependency) -> list[Task]:
    return service.list_tasks()


def get_task(task_id: int, service: TaskServiceDependency) -> Task:
    return service.get_task(task_id)


def update_task(
    task_id: int, data: TaskUpdate, service: TaskServiceDependency
) -> Task:
    return service.update_task(task_id, data.get("title"), data.get("description"), data.get("status"))


def delete_task(task_id: int, service: TaskServiceDependency) -> DeleteTaskResponse:
    service.delete_task(task_id)
    return DeleteTaskResponse(message="Task deleted")
