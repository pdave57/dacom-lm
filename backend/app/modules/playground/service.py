import uuid

from app.modules.playground.schemas import (
    ExecutionResponse,
    FrontendExecuteRequest,
    PythonExecuteRequest,
    SQLExecuteRequest,
)
from app.shared.enums import ExecutionStatus


class PlaygroundService:
    @staticmethod
    def enqueue_frontend(payload: FrontendExecuteRequest) -> ExecutionResponse:
        return ExecutionResponse(job_id=uuid.uuid4(), status=ExecutionStatus.QUEUED.value)

    @staticmethod
    def enqueue_python(payload: PythonExecuteRequest) -> ExecutionResponse:
        return ExecutionResponse(job_id=uuid.uuid4(), status=ExecutionStatus.QUEUED.value)

    @staticmethod
    def enqueue_sql(payload: SQLExecuteRequest) -> ExecutionResponse:
        return ExecutionResponse(job_id=uuid.uuid4(), status=ExecutionStatus.QUEUED.value)
