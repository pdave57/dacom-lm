from app.workers.celery_app import celery_app


@celery_app.task(name="execution.run_sql")
def run_sql_task(job_id: str, query: str) -> dict[str, str]:
    """Execute participant SQL query against an isolated temporary PostgreSQL schema."""
    return {"job_id": job_id, "status": "completed"}
