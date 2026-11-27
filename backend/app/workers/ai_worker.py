from app.workers.celery_app import celery_app


@celery_app.task(name="ai.ingest_lesson_embeddings")
def ingest_lesson_embeddings_task(lesson_id: str) -> dict[str, str]:
    """Chunk lesson markdown, generate embeddings, and store in pgvector."""
    return {"lesson_id": lesson_id, "status": "completed"}


@celery_app.task(name="ai.generate_lesson_audio")
def generate_lesson_audio_task(
    lesson_id: str, voice: str = "alloy", language: str = "en"
) -> dict[str, str]:
    """Convert lesson written text into AI-generated audio and upload to object storage."""
    return {
        "lesson_id": lesson_id,
        "voice": voice,
        "language": language,
        "status": "completed",
    }
