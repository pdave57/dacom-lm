import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LessonChatRequest(BaseModel):
    message: str
    conversation_id: Optional[uuid.UUID] = None


class LessonChatResponse(BaseModel):
    conversation_id: uuid.UUID
    answer: str
    references: list[str] = []
    task_id: Optional[str] = None


class AIConversationResponse(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    title: Optional[str] = None
    created_at: datetime


class AIMessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
