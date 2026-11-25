import uuid

from fastapi import APIRouter, Depends, status

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.mentorship.schemas import (
    MentorResponse,
    MentorshipMessageCreate,
    MentorshipRequestCreate,
    MentorshipRequestResponse,
)
from app.modules.mentorship.service import MentorshipService
from app.shared.responses import MessageResponse

router = APIRouter(prefix="/mentorship", tags=["Remote Code Mentorship"])


@router.post("/requests", response_model=MentorshipRequestResponse, status_code=status.HTTP_201_CREATED)
def create_mentorship_request(
    payload: MentorshipRequestCreate,
    current_user: CurrentUser = Depends(get_current_user),
) -> MentorshipRequestResponse:
    return MentorshipService.create_request(payload)


@router.get("/requests/{request_id}", response_model=MentorshipRequestResponse)
def get_mentorship_request(
    request_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> MentorshipRequestResponse:
    return MentorshipRequestResponse(
        id=request_id,
        title="Sample Mentorship Request",
        description="Scaffold detail view",
        status="submitted",
    )


@router.post("/requests/{request_id}/messages", response_model=MessageResponse)
def add_mentorship_message(
    request_id: uuid.UUID,
    payload: MentorshipMessageCreate,
    current_user: CurrentUser = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(message=f"Message added to mentorship request {request_id}")


@router.post("/requests/{request_id}/resolve", response_model=MessageResponse)
def resolve_mentorship_request(
    request_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> MessageResponse:
    return MessageResponse(message=f"Mentorship request {request_id} resolved")


@router.get("/mentors", response_model=list[MentorResponse])
def list_mentors(current_user: CurrentUser = Depends(get_current_user)) -> list[MentorResponse]:
    return []
