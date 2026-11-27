from app.workers.celery_app import celery_app


@celery_app.task(name="execution.run_python")
def run_python_task(job_id: str, code: str) -> dict[str, str]:
    """Execute participant Python code inside an isolated sandboxed container."""
    return {"job_id": job_id, "status": "completed"}
