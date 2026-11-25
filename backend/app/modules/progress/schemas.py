import uuid

from pydantic import BaseModel


class LessonProgressUpdate(BaseModel):
    lesson_id: uuid.UUID
    is_completed: bool = False
    video_position_seconds: int = 0


class LessonProgressResponse(BaseModel):
    lesson_id: uuid.UUID
    is_completed: bool
    video_position_seconds: int
