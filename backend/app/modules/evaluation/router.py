import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.evaluation.schemas import EvaluationSummaryResponse
from app.modules.evaluation.service import EvaluationService

router = APIRouter(prefix="/evaluations", tags=["Evaluation & Scoring"])


@router.get("/submissions/{submission_id}", response_model=EvaluationSummaryResponse)
def get_evaluation_summary(
    submission_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> EvaluationSummaryResponse:
    return EvaluationService.get_summary(submission_id)
