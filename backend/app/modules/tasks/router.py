"""Router for querying the status/result of Celery background jobs.

Clients poll ``GET /api/v1/tasks/{task_id}`` after enqueuing a background
job (AI explanation, code execution, raid inspection, etc.) to retrieve the
outcome once the worker has finished processing.
"""

from typing import Any

from fastapi import APIRouter

from app.workers.celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=["Background Tasks"])


@router.get("/{task_id}")
def get_task_status(task_id: str) -> dict[str, Any]:
    """Return the current state and result of a Celery task."""
    async_result = celery_app.AsyncResult(task_id)

    response: dict[str, Any] = {
        "task_id": task_id,
        "status": async_result.status,
    }

    if async_result.state == "SUCCESS":
        response["result"] = async_result.result
    elif async_result.state == "FAILURE":
        response["error"] = str(async_result.info)
    elif async_result.state in ("RETRY", "REVOKED"):
        response["info"] = str(async_result.info)

    return response
