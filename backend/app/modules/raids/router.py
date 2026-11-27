import uuid
from typing import Any

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.raids.schemas import (
    RaidResponse,
    RaidReviewRequest,
    RaidSubmissionResponse,
    RaidSubmitRequest,
)
from app.modules.raids.service import RaidService
from app.shared.enums import RoleEnum
from app.shared.responses import MessageResponse
from app.workers.tasks import evaluate_raid_submission, inspect_raid_submission

router = APIRouter(prefix="/raids", tags=["Raids"])


@router.get("", response_model=list[RaidResponse])
def list_raids(current_user: CurrentUser = Depends(get_current_user)) -> list[RaidResponse]:
    return []


@router.post("/{raid_id}/submit", response_model=RaidSubmissionResponse)
def submit_raid(
    raid_id: uuid.UUID,
    payload: RaidSubmitRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> RaidSubmissionResponse:
    return RaidService.submit_raid(raid_id, payload)


@router.get("/submissions", response_model=list[RaidSubmissionResponse])
def list_raid_submissions(
    current_user: CurrentUser = Depends(get_current_user),
) -> list[RaidSubmissionResponse]:
    return []


@router.post("/submissions/{submission_id}/inspect")
def trigger_raid_inspection(
    submission_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> dict[str, Any]:
    """Queue an automated inspection of a raid submission as a background job."""
    task = inspect_raid_submission.delay(str(submission_id))
    return {
        "task_id": str(task.id),
        "message": f"Automated inspection queued for submission {submission_id}",
    }


@router.post("/submissions/{submission_id}/review")
def review_raid_submission(
    submission_id: uuid.UUID,
    payload: RaidReviewRequest,
    current_user: CurrentUser = Depends(
        require_roles(RoleEnum.PROJECT_EVALUATOR, RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN)
    ),
) -> dict[str, Any]:
    """Queue an evaluation of a raid submission as a background job."""
    task = evaluate_raid_submission.delay(str(submission_id))
    return {
        "task_id": str(task.id),
        "message": f"Evaluation queued for submission {submission_id}",
    }
