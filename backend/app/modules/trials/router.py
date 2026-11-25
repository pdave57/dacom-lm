import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.trials.schemas import (
    TrialExecuteRequest,
    TrialResponse,
    TrialResultResponse,
    TrialStartResponse,
    TrialSubmitRequest,
)
from app.modules.trials.service import TrialService
from app.shared.responses import MessageResponse

router = APIRouter(prefix="/trials", tags=["Trials"])


@router.get("", response_model=list[TrialResponse])
def list_trials(current_user: CurrentUser = Depends(get_current_user)) -> list[TrialResponse]:
    return []


@router.post("/{trial_id}/start", response_model=TrialStartResponse)
def start_trial(
    trial_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> TrialStartResponse:
    return TrialService.start_trial(trial_id)


@router.post("/{trial_id}/execute", response_model=MessageResponse)
def execute_trial_code(
    trial_id: uuid.UUID,
    payload: TrialExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(message=f"Execution queued for trial {trial_id}")


@router.post("/{trial_id}/submit", response_model=TrialResultResponse)
def submit_trial(
    trial_id: uuid.UUID,
    payload: TrialSubmitRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> TrialResultResponse:
    return TrialService.get_result(payload.attempt_id)


@router.get("/attempts/{attempt_id}/result", response_model=TrialResultResponse)
def get_trial_result(
    attempt_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> TrialResultResponse:
    return TrialService.get_result(attempt_id)
