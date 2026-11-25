import uuid

from app.modules.inspection.schemas import InspectionStatusResponse


class InspectionService:
    @staticmethod
    def get_status(submission_id: uuid.UUID) -> InspectionStatusResponse:
        return InspectionStatusResponse(
            inspection_id=uuid.uuid4(),
            submission_id=submission_id,
            status="queued",
        )
