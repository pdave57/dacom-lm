import uuid

from app.modules.evaluation.schemas import EvaluationSummaryResponse


class EvaluationService:
    @staticmethod
    def get_summary(submission_id: uuid.UUID) -> EvaluationSummaryResponse:
        return EvaluationSummaryResponse(
            submission_id=submission_id,
            total_score=0.0,
            status="pending",
        )
