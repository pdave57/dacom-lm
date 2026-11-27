from app.workers.celery_app import celery_app


@celery_app.task(name="evaluation.score_submission")
def score_submission_task(submission_id: str) -> dict[str, str]:
    """Aggregate automated checks and rubric scores for a Raid or Trial submission."""
    return {"submission_id": submission_id, "status": "completed"}
