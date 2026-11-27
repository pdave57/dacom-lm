import uuid

from app.modules.python_execution.schemas import PythonSandboxRequest, PythonSandboxResult
from app.shared.enums import ExecutionStatus
from app.workers.tasks import execute_python_code


class PythonExecutionService:
    @staticmethod
    def submit(payload: PythonSandboxRequest) -> PythonSandboxResult:
        """Queue Python code execution as a background job.

        Runs untrusted code in an isolated sandbox via a Celery worker so the
        API request returns immediately.
        """
        job_id = uuid.uuid4()
        task = execute_python_code.delay(
            job_id=str(job_id),
            code=payload.code,
            timeout_seconds=payload.timeout_seconds,
        )

        return PythonSandboxResult(
            job_id=job_id,
            status=ExecutionStatus.QUEUED.value,
            task_id=str(task.id),
        )
