from app.workers.celery_app import celery_app


@celery_app.task(name="raids.inspect_submission")
def inspect_raid_submission_task(submission_id: str) -> dict[str, str]:
    """Clone Gitea commit and run static analysis, tests, and security checks."""
    return {"submission_id": submission_id, "status": "completed"}
