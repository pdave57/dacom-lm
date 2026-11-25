from enum import StrEnum


class RoleEnum(StrEnum):
    SUPER_ADMIN = "super_administrator"
    ADMIN = "administrator"
    CONTENT_MANAGER = "academic_content_manager"
    MENTOR = "remote_code_mentor"
    ASSESSMENT_MANAGER = "assessment_manager"
    PROJECT_EVALUATOR = "project_evaluator"
    PARTICIPANT = "participant"


class ContentStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class TrialLanguage(StrEnum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    REACT = "react"
    SQL = "sql"


class TrialQuestionType(StrEnum):
    MCQ = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    PYTHON_CODING = "python_coding"
    JS_CODING = "javascript_coding"
    TS_CODING = "typescript_coding"
    REACT_CHALLENGE = "react_challenge"
    SQL_QUERY = "sql_query"
    DEBUGGING = "debugging"
    CODE_COMPLETION = "code_completion"
    API_CHALLENGE = "api_challenge"
    DATABASE_DESIGN = "database_design"


class MentorshipStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    AWAITING_ASSIGNMENT = "awaiting_assignment"
    ASSIGNED = "assigned"
    IN_REVIEW = "in_review"
    AWAITING_PARTICIPANT_RESPONSE = "awaiting_participant_response"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ExecutionStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class CertificateStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
