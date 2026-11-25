from dataclasses import replace
from threading import Lock

from app.domain.task import Task, TaskStatus


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        # FastAPI can run synchronous endpoints in different threads.
        self._lock = Lock()

    def add_task(self, title: str, description: str) -> Task:
        with self._lock:
            task = Task(self._next_id, title, description)
            self._tasks[task.id] = task
            self._next_id += 1
            return task

    def list_tasks(self) -> list[Task]:
        with self._lock:
            return list(self._tasks.values())

    def find_task(self, task_id: int) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def update_task(
        self, task_id: int, title: str | None, description: str | None,
        status: TaskStatus | None,
    ) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None

            updated_task = replace(
                task,
                title=task.title if title is None else title,
                description=task.description if description is None else description,
                status=task.status if status is None else status,
            )
            self._tasks[task_id] = updated_task
            return updated_task

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None
