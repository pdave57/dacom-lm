import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, get_current_user
from app.database.session import get_db
from app.modules.ai_tutor.schemas import (
    AIConversationResponse,
    AIMessageResponse,
    LessonChatRequest,
    LessonChatResponse,
)
from app.modules.ai_tutor.service import AITutorService

router = APIRouter(prefix="/ai", tags=["AI Tutor"])


@router.post("/lessons/{lesson_id}/chat", response_model=LessonChatResponse)
def chat_with_lesson(
    lesson_id: uuid.UUID,
    payload: LessonChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonChatResponse:
    return AITutorService.chat_with_lesson(db, current_user.user_id, lesson_id, payload)


@router.get("/conversations", response_model=list[AIConversationResponse])
def list_conversations(
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AIConversationResponse]:
    return []


@router.get("/conversations/{conversation_id}/messages", response_model=list[AIMessageResponse])
def list_conversation_messages(
    conversation_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AIMessageResponse]:
    return []
