from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import InvalidTitleError, TaskNotFoundError


async def task_not_found_handler(
    _request: Request, _error: TaskNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Task not found"})


async def invalid_title_handler(
    _request: Request, _error: InvalidTitleError
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": "Title cannot be empty"})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
    app.add_exception_handler(InvalidTitleError, invalid_title_handler)
