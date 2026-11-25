from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.playground.schemas import (
    ExecutionResponse,
    FrontendExecuteRequest,
    PythonExecuteRequest,
    SQLExecuteRequest,
)
from app.modules.playground.service import PlaygroundService

router = APIRouter(prefix="/playground", tags=["Coding Playground"])


@router.post("/frontend/execute", response_model=ExecutionResponse)
def execute_frontend(
    payload: FrontendExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ExecutionResponse:
    return PlaygroundService.enqueue_frontend(payload)


@router.post("/python/execute", response_model=ExecutionResponse)
def execute_python(
    payload: PythonExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ExecutionResponse:
    return PlaygroundService.enqueue_python(payload)


@router.post("/sql/execute", response_model=ExecutionResponse)
def execute_sql(
    payload: SQLExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ExecutionResponse:
    return PlaygroundService.enqueue_sql(payload)
