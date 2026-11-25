import uuid

from app.modules.mentorship.schemas import MentorshipRequestCreate, MentorshipRequestResponse
from app.shared.enums import MentorshipStatus


class MentorshipService:
    @staticmethod
    def create_request(payload: MentorshipRequestCreate) -> MentorshipRequestResponse:
        return MentorshipRequestResponse(
            id=uuid.uuid4(),
            title=payload.title,
            description=payload.description,
            status=MentorshipStatus.SUBMITTED.value,
        )
