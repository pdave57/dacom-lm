from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.python_execution.schemas import PythonSandboxRequest, PythonSandboxResult
from app.modules.python_execution.service import PythonExecutionService

router = APIRouter(prefix="/python-execution", tags=["Python Execution"])


@router.post("/run", response_model=PythonSandboxResult)
def run_python(
    payload: PythonSandboxRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> PythonSandboxResult:
    return PythonExecutionService.submit(payload)
