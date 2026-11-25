from app.domain.task import Task, TaskStatus
from app.exceptions import InvalidTitleError, TaskNotFoundError
from app.repositories.task_repository import InMemoryTaskRepository


class TaskService:
    def __init__(self, repository: InMemoryTaskRepository) -> None:
        self._repository = repository

    def create_task(self, title: str, description: str) -> Task:
        return self._repository.add_task(self._validate_title(title), description)

    def list_tasks(self) -> list[Task]:
        return self._repository.list_tasks()

    def get_task(self, task_id: int) -> Task:
        task = self._repository.find_task(task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

    def update_task(
        self, task_id: int, title: str | None, description: str | None,
        status: TaskStatus | None,
    ) -> Task:
        if title is not None:
            self.get_task(task_id)
            title = self._validate_title(title)

        task = self._repository.update_task(task_id, title, description, status)
        if task is None:
            raise TaskNotFoundError()
        return task

    def delete_task(self, task_id: int) -> None:
        if not self._repository.delete_task(task_id):
            raise TaskNotFoundError()

    @staticmethod
    def _validate_title(title: str) -> str:
        clean_title = title.strip()
        if not clean_title:
            raise InvalidTitleError()
        return clean_title
