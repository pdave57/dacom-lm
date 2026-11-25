from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.sql_execution.schemas import SQLSandboxRequest, SQLSandboxResult
from app.modules.sql_execution.service import SQLExecutionService

router = APIRouter(prefix="/sql-execution", tags=["SQL Execution"])


@router.post("/run", response_model=SQLSandboxResult)
def run_sql(
    payload: SQLSandboxRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> SQLSandboxResult:
    return SQLExecutionService.submit(payload)
