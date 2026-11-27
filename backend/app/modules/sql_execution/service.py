import uuid

from sqlalchemy.orm import Session

from app.modules.sql_execution.models import SQLExecutionJob
from app.modules.sql_execution.schemas import SQLSandboxRequest, SQLSandboxResult
from app.shared.enums import ExecutionStatus
from app.workers.tasks import execute_sql_query


class SQLExecutionService:
    @staticmethod
    def submit(
        db: Session, user_id: str, payload: SQLSandboxRequest
    ) -> SQLSandboxResult:
        """Queue a SQL query execution as a background job.

        Persists a ``SQLExecutionJob`` row so the client can poll for
        completion, then hands the work to a Celery worker.
        """
        job_id = uuid.uuid4()
        user_uuid = uuid.UUID(user_id)

        job = SQLExecutionJob(
            id=job_id,
            user_id=user_uuid,
            query=payload.query,
            status=ExecutionStatus.QUEUED.value,
        )
        db.add(job)
        db.commit()

        task = execute_sql_query.delay(
            job_id=str(job_id),
            user_id=str(user_uuid),
            query=payload.query,
            dataset_id=str(payload.dataset_id) if payload.dataset_id else None,
        )

        return SQLSandboxResult(
            job_id=job_id,
            status=ExecutionStatus.QUEUED.value,
            task_id=str(task.id),
        )
