import uuid

from sqlalchemy.orm import Session

from app.modules.ai_tutor.schemas import LessonChatRequest, LessonChatResponse


class AITutorService:
    @staticmethod
    def chat_with_lesson(
        db: Session, user_id: str, lesson_id: uuid.UUID, payload: LessonChatRequest
    ) -> LessonChatResponse:
        # TODO: Retrieve pgvector lesson chunks and query LLM provider.
        return LessonChatResponse(
            conversation_id=payload.conversation_id or uuid.uuid4(),
            answer="AI Tutor scaffold response grounded in lesson materials.",
            references=[str(lesson_id)],
        )
