from fastapi import FastAPI

from app.exception_handlers import register_exception_handlers
from app.repositories.task_repository import InMemoryTaskRepository
from app.routers.task_router import router
from app.services.task_service import TaskService


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager API")
    app.state.task_service = TaskService(InMemoryTaskRepository())
    register_exception_handlers(app)
    app.include_router(router)
    return app


app = create_app()
