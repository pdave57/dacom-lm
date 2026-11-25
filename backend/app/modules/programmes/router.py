from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.programmes.schemas import ProgrammeResponse
from app.shared.pagination import PaginationParams

router = APIRouter(prefix="/programmes", tags=["Programmes"])


@router.get("", response_model=list[ProgrammeResponse])
def list_programmes(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[ProgrammeResponse]:
    return []
