import uuid

from app.modules.python_execution.schemas import PythonSandboxRequest, PythonSandboxResult
from app.shared.enums import ExecutionStatus


class PythonExecutionService:
    @staticmethod
    def submit(payload: PythonSandboxRequest) -> PythonSandboxResult:
        return PythonSandboxResult(job_id=uuid.uuid4(), status=ExecutionStatus.QUEUED.value)
