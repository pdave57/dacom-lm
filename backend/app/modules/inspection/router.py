import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.inspection.schemas import InspectionStatusResponse
from app.modules.inspection.service import InspectionService

router = APIRouter(prefix="/inspections", tags=["Automated Inspection"])


@router.get("/submissions/{submission_id}", response_model=InspectionStatusResponse)
def get_inspection_status(
    submission_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> InspectionStatusResponse:
    return InspectionService.get_status(submission_id)
