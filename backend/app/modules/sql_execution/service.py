import uuid

from app.modules.sql_execution.schemas import SQLSandboxRequest, SQLSandboxResult
from app.shared.enums import ExecutionStatus


class SQLExecutionService:
    @staticmethod
    def submit(payload: SQLSandboxRequest) -> SQLSandboxResult:
        return SQLSandboxResult(job_id=uuid.uuid4(), status=ExecutionStatus.QUEUED.value)
