"""Celery application configuration for Dacom-LM background jobs.

Tasks are defined in ``app.workers.tasks`` and executed by the
``celery -A app.workers.celery_app worker`` command (see docker-compose).
"""

from celery import Celery
from kombu import Exchange, Queue

from app.core.config import settings

celery_app = Celery(
    "dacom_lm",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,  # results expire after 1 hour
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    worker_send_task_events=True,
    task_send_sent_event=True,
    task_default_queue="default",
    task_routes={
        # AI / LLM work (slow, I/O bound)
        "app.workers.tasks.generate_ai_explanation": {"queue": "ai"},
        # Isolated code execution
        "app.workers.tasks.execute_python_code": {"queue": "python"},
        "app.workers.tasks.execute_sql_query": {"queue": "sql"},
        # Project (Raid) inspection & evaluation
        "app.workers.tasks.inspect_raid_submission": {"queue": "inspection"},
        "app.workers.tasks.evaluate_raid_submission": {"queue": "evaluation"},
        # Outbound notifications / email
        "app.workers.tasks.send_notification": {"queue": "notifications"},
    },
    task_queues=(
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("ai", Exchange("ai"), routing_key="ai"),
        Queue("python", Exchange("python"), routing_key="python"),
        Queue("sql", Exchange("sql"), routing_key="sql"),
        Queue("inspection", Exchange("inspection"), routing_key="inspection"),
        Queue("evaluation", Exchange("evaluation"), routing_key="evaluation"),
        Queue("notifications", Exchange("notifications"), routing_key="notifications"),
    ),
)

__all__ = ["celery_app"]
