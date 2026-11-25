from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.learning_paths.schemas import LearningPathResponse
from app.shared.pagination import PaginationParams

router = APIRouter(prefix="/learning-paths", tags=["Learning Paths"])


@router.get("", response_model=list[LearningPathResponse])
def list_learning_paths(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[LearningPathResponse]:
    return []
