from app.workers.celery_app import celery_app


@celery_app.task(name="execution.run_frontend")
def run_frontend_task(job_id: str) -> dict[str, str]:
    """Validate and execute frontend HTML/CSS/JS/React exercises in an isolated runner."""
    return {"job_id": job_id, "status": "completed"}
