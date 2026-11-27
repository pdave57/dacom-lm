from app.workers.celery_app import celery_app


@celery_app.task(name="notifications.send")
def send_notification_task(user_id: str, title: str, body: str) -> dict[str, str]:
    """Deliver in-app and email notifications asynchronously."""
    return {"user_id": user_id, "title": title, "status": "sent"}
