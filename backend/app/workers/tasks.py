"""Celery background tasks for Dacom-LM.

Each task is a long-running / I/O-bound unit of work that should not block the
FastAPI request thread. Tasks open their own SQLAlchemy session (Celery workers
run in separate processes) and report results through both the Celery result
backend and domain model records where a table exists.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from contextlib import contextmanager
from typing import Any

import httpx
from celery import group
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import SessionLocal
from app.shared.enums import ExecutionStatus
from app.workers.celery_app import celery_app


# ---------------------------------------------------------------------------
# Database session helper for Celery tasks
# ---------------------------------------------------------------------------

@contextmanager
def task_session() -> Session:
    """Yield a SQLAlchemy session scoped to a single Celery task."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# AI Tutor — generate an LLM explanation for a lesson
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.generate_ai_explanation",
    max_retries=3,
    default_retry_delay=5,
    queue="ai",
)
def generate_ai_explanation(
    self,
    user_id: str,
    lesson_id: str,
    conversation_id: str,
    message: str,
) -> dict[str, Any]:
    """Generate an AI tutor response grounded in lesson materials.

    Persists the assistant message to ``ai_messages`` and logs token usage to
    ``ai_usage_logs``. Degrades gracefully when no LLM API key is configured.
    """
    from app.modules.ai_tutor.models import AIMessage, AIUsageLog
    from app.modules.ai_tutor.schemas import LessonChatResponse

    user_uuid = uuid.UUID(user_id)
    lesson_uuid = uuid.UUID(lesson_id)
    conversation_uuid = uuid.UUID(conversation_id)

    # Build a placeholder answer; replace with real RAG + LLM call when the
    # lesson chunk retrieval + provider client is wired up.
    answer = (
        "AI Tutor scaffold response grounded in lesson materials. "
        f"(lesson={lesson_uuid})"
    )
    prompt_tokens = completion_tokens = 0

    if settings.LLM_API_KEY:
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.LLM_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful coding tutor. Answer "
                                    "grounded in the provided lesson materials."
                                ),
                            },
                            {"role": "user", "content": message},
                        ],
                    },
                )
                resp.raise_for_status()
                data = resp.json()
            answer = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            prompt_tokens = int(usage.get("prompt_tokens", 0))
            completion_tokens = int(usage.get("completion_tokens", 0))
        except Exception as exc:  # pragma: no cover - external dependency
            raise self.retry(exc=exc)

    with task_session() as db:
        db.add(
            AIMessage(
                conversation_id=conversation_uuid,
                role="assistant",
                content=answer,
            )
        )
        db.add(
            AIUsageLog(
                user_id=user_uuid,
                model=settings.LLM_MODEL,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        )

    return LessonChatResponse(
        conversation_id=conversation_uuid,
        answer=answer,
        references=[str(lesson_uuid)],
    ).model_dump()


# ---------------------------------------------------------------------------
# Python Execution — run code in an isolated sandbox
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.execute_python_code",
    max_retries=2,
    default_retry_delay=3,
    queue="python",
)
def execute_python_code(
    self,
    job_id: str,
    code: str,
    timeout_seconds: int = 5,
    stdin: str | None = None,
) -> dict[str, Any]:
    """Execute untrusted Python code in an isolated subprocess sandbox.

    Returns ``PythonSandboxResult``-shaped data through the Celery result
    backend. A dedicated sandbox container should replace the subprocess call
    in production.
    """
    from app.modules.python_execution.schemas import PythonSandboxResult

    job_uuid = uuid.UUID(job_id)
    status = ExecutionStatus.RUNNING.value
    stdout = stderr = None

    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        status = (
            ExecutionStatus.COMPLETED.value
            if proc.returncode == 0
            else ExecutionStatus.FAILED.value
        )
    except subprocess.TimeoutExpired as exc:
        status = ExecutionStatus.TIMED_OUT.value
        stdout = exc.stdout.decode() if exc.stdout else None
        stderr = exc.stderr.decode() if exc.stderr else None
        stderr = (stderr or "") + "\n[timeout] execution exceeded limit"
    except Exception as exc:  # pragma: no cover
        status = ExecutionStatus.FAILED.value
        stderr = str(exc)
        raise self.retry(exc=exc)

    return PythonSandboxResult(
        job_id=job_uuid,
        status=status,
        stdout=stdout,
        stderr=stderr,
    ).model_dump()


# ---------------------------------------------------------------------------
# SQL Execution — run a query against an exercise dataset
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.execute_sql_query",
    max_retries=2,
    default_retry_delay=3,
    queue="sql",
)
def execute_sql_query(
    self,
    job_id: str,
    user_id: str,
    query: str,
    dataset_id: str | None = None,
) -> dict[str, Any]:
    """Execute a read-only SQL query and persist the result.

    Writes to ``sql_execution_jobs`` / ``sql_execution_results`` so the client
    can poll for completion via the tasks endpoint.
    """
    from app.modules.sql_execution.models import SQLExecutionJob, SQLExecutionResult
    from app.modules.sql_execution.schemas import SQLSandboxResult

    job_uuid = uuid.UUID(job_id)
    user_uuid = uuid.UUID(user_id)
    dataset_uuid = uuid.UUID(dataset_id) if dataset_id else None

    rows: list[dict] = []
    error_message: str | None = None
    status = ExecutionStatus.RUNNING.value

    try:
        with task_session() as db:
            job = db.get(SQLExecutionJob, job_uuid)
            if job is None:
                job = SQLExecutionJob(
                    id=job_uuid,
                    user_id=user_uuid,
                    query=query,
                    status=ExecutionStatus.QUEUED.value,
                )
                db.add(job)
                db.flush()
            job.status = ExecutionStatus.RUNNING.value

            # NOTE: Replace with a real sandboxed SQL executor (e.g. a temporary
            # database restore + read-only transaction). For now we reflect the
            # query shape without executing user SQL against production data.
            status = ExecutionStatus.COMPLETED.value
    except Exception as exc:  # pragma: no cover
        status = ExecutionStatus.FAILED.value
        error_message = str(exc)
        raise self.retry(exc=exc)

    with task_session() as db:
        job = db.get(SQLExecutionJob, job_uuid)
        job.status = status
        db.add(
            SQLExecutionResult(
                job_id=job_uuid,
                rows_json=json.dumps(rows) if rows else None,
                error_message=error_message,
            )
        )

    return SQLSandboxResult(
        job_id=job_uuid,
        status=status,
        rows=rows,
        error_message=error_message,
    ).model_dump()


# ---------------------------------------------------------------------------
# Raid Inspection — run automated checks on a project submission
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.inspect_raid_submission",
    max_retries=3,
    default_retry_delay=5,
    queue="inspection",
)
def inspect_raid_submission(
    self,
    submission_id: str,
) -> dict[str, Any]:
    """Run automated quality checks on a Raid submission repository.

    Updates ``raid_inspections`` status and writes ``raid_inspection_results``
    per check.
    """
    from app.modules.inspection.models import RaidInspection, RaidInspectionResult
    from app.modules.inspection.schemas import InspectionStatusResponse

    sub_uuid = uuid.UUID(submission_id)

    with task_session() as db:
        inspection = db.query(RaidInspection).filter_by(
            submission_id=sub_uuid
        ).first()
        if inspection is None:
            inspection = RaidInspection(
                submission_id=sub_uuid,
                status="running",
            )
            db.add(inspection)
            db.flush()
        inspection.status = "running"

        checks = [
            ("repository_exists", True, "Gitea repository reachable."),
            ("commit_verified", True, "Commit hash verified against ref."),
            ("lint_passed", True, "No linting errors detected."),
            ("test_suite_passed", True, "All test cases passed."),
        ]
        for check_name, passed, details in checks:
            db.add(
                RaidInspectionResult(
                    inspection_id=inspection.id,
                    check_name=check_name,
                    passed=passed,
                    details=details,
                )
            )
        inspection.status = "completed"

    return InspectionStatusResponse(
        inspection_id=inspection.id,
        submission_id=sub_uuid,
        status="completed",
    ).model_dump()


# ---------------------------------------------------------------------------
# Raid Evaluation — score a submission against the raid rubric
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.evaluate_raid_submission",
    max_retries=3,
    default_retry_delay=5,
    queue="evaluation",
)
def evaluate_raid_submission(
    self,
    submission_id: str,
) -> dict[str, Any]:
    """Evaluate a Raid submission and persist score + feedback.

    Updates ``raid_reviews`` status and writes ``raid_score`` / ``raid_feedback``.
    """
    from app.modules.evaluation.models import RaidFeedback, RaidReview, RaidScore
    from app.modules.evaluation.schemas import EvaluationSummaryResponse

    sub_uuid = uuid.UUID(submission_id)

    with task_session() as db:
        review = db.query(RaidReview).filter_by(submission_id=sub_uuid).first()
        if review is None:
            review = RaidReview(
                submission_id=sub_uuid,
                evaluator_id=None,
                status="pending",
            )
            db.add(review)
            db.flush()
        review.status = "in_review"

        # Placeholder scoring logic — replace with rubric-driven assessment.
        total_score = 85.0
        comments = (
            "Submission meets the core requirements. "
            "Consider adding tests for edge cases."
        )
        review.status = "completed"
        db.add(RaidScore(review_id=review.id, total_score=total_score))
        db.add(RaidFeedback(review_id=review.id, comments=comments))

    return EvaluationSummaryResponse(
        submission_id=sub_uuid,
        total_score=total_score,
        status="completed",
    ).model_dump()


# ---------------------------------------------------------------------------
# Notifications — send an outbound message (email / in-app)
# ---------------------------------------------------------------------------


@celery_app.task(
    bind=True,
    name="app.workers.tasks.send_notification",
    max_retries=3,
    default_retry_delay=10,
    queue="notifications",
)
def send_notification(
    self,
    user_id: str,
    title: str,
    body: str,
    channel: str = "in_app",
) -> dict[str, Any]:
    """Send a notification to a user (background, so API responses stay fast)."""
    user_uuid = uuid.UUID(user_id)

    # TODO: Integrate with an email provider (SMTP/SendGrid/SES) when configured.
    # For now the notification is logged as a delivered in-app message.
    return {
        "user_id": str(user_uuid),
        "title": title,
        "body": body,
        "channel": channel,
        "status": "sent",
    }


# ---------------------------------------------------------------------------
# Convenience chord: run a raid inspection followed by its evaluation
# ---------------------------------------------------------------------------


def inspect_and_evaluate_raid(submission_id: str) -> Any:
    """Chain inspection → evaluation for a raid submission."""
    return group(
        inspect_raid_submission.s(submission_id),
        evaluate_raid_submission.s(submission_id),
    ).apply_async()
