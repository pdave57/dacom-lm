from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.database.session import get_db
from app.modules.sql_execution.schemas import SQLSandboxRequest, SQLSandboxResult
from app.modules.sql_execution.service import SQLExecutionService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sql-execution", tags=["SQL Execution"])


@router.post("/run", response_model=SQLSandboxResult)
def run_sql(
    payload: SQLSandboxRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SQLSandboxResult:
    return SQLExecutionService.submit(db, current_user.user_id, payload)
