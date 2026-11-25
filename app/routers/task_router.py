from fastapi import APIRouter, status

from app.controllers import task_controller
from app.schemas.task_schema import DeleteTaskResponse, TaskResponse

router = APIRouter()
tasks = APIRouter(prefix="/tasks", tags=["Tasks"])

# Each route connects an HTTP method and path to a controller function.
tasks.add_api_route(
    "", task_controller.create_task, methods=["POST"],
    response_model=TaskResponse, status_code=status.HTTP_201_CREATED,
)
tasks.add_api_route(
    "", task_controller.list_tasks, methods=["GET"], response_model=list[TaskResponse],
)
tasks.add_api_route(
    "/{task_id}", task_controller.get_task, methods=["GET"], response_model=TaskResponse,
)
tasks.add_api_route(
    "/{task_id}", task_controller.update_task, methods=["PATCH"],
    response_model=TaskResponse,
)
tasks.add_api_route(
    "/{task_id}", task_controller.delete_task, methods=["DELETE"],
    response_model=DeleteTaskResponse,
)
router.include_router(tasks)
