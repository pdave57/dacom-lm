import uuid

from sqlalchemy.orm import Session

from app.modules.ai_tutor.schemas import LessonChatRequest, LessonChatResponse
from app.workers.tasks import generate_ai_explanation


class AITutorService:
    @staticmethod
    def chat_with_lesson(
        db: Session, user_id: str, lesson_id: uuid.UUID, payload: LessonChatRequest
    ) -> LessonChatResponse:
        """Queue an AI tutor explanation as a background job.

        The LLM call is slow and I/O bound, so it runs in a Celery worker
        instead of blocking the HTTP request thread. The client can poll the
        ``/api/v1/tasks/{task_id}`` endpoint for the result.
        """
        conversation_id = payload.conversation_id or uuid.uuid4()

        task = generate_ai_explanation.delay(
            user_id=str(user_id),
            lesson_id=str(lesson_id),
            conversation_id=str(conversation_id),
            message=payload.message,
        )

        return LessonChatResponse(
            conversation_id=conversation_id,
            answer="Your request is being processed in the background.",
            references=[str(lesson_id)],
            task_id=str(task.id),
        )
