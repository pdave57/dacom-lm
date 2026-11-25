from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.administration.router import router as administration_router
from app.modules.ai_tutor.router import router as ai_tutor_router
from app.modules.analytics.router import router as analytics_router
from app.modules.auth.router import router as auth_router
from app.modules.certification.router import router as certification_router
from app.modules.courses.router import router as courses_router
from app.modules.evaluation.router import router as evaluation_router
from app.modules.gitea.router import router as gitea_router
from app.modules.inspection.router import router as inspection_router
from app.modules.learning_paths.router import router as learning_paths_router
from app.modules.lessons.router import router as lessons_router
from app.modules.mentorship.router import router as mentorship_router
from app.modules.playground.router import router as playground_router
from app.modules.programmes.router import router as programmes_router
from app.modules.progress.router import router as progress_router
from app.modules.python_execution.router import router as python_execution_router
from app.modules.raids.router import router as raids_router
from app.modules.roles.router import router as roles_router
from app.modules.sql_execution.router import router as sql_execution_router
from app.modules.trials.router import router as trials_router
from app.modules.users.router import router as users_router


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Dacom-LM — Self-Paced Software Engineering Learning & Assessment Platform",
        version="1.2.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "service": settings.APP_NAME}

    api_v1 = APIRouter(prefix=settings.API_V1_PREFIX)
    api_v1.include_router(auth_router)
    api_v1.include_router(users_router)
    api_v1.include_router(roles_router)
    api_v1.include_router(programmes_router)
    api_v1.include_router(learning_paths_router)
    api_v1.include_router(courses_router)
    api_v1.include_router(lessons_router)
    api_v1.include_router(progress_router)
    api_v1.include_router(ai_tutor_router)
    api_v1.include_router(playground_router)
    api_v1.include_router(trials_router)
    api_v1.include_router(python_execution_router)
    api_v1.include_router(sql_execution_router)
    api_v1.include_router(raids_router)
    api_v1.include_router(gitea_router)
    api_v1.include_router(inspection_router)
    api_v1.include_router(evaluation_router)
    api_v1.include_router(mentorship_router)
    api_v1.include_router(certification_router)
    api_v1.include_router(analytics_router)
    api_v1.include_router(administration_router)

    app.include_router(api_v1)
    return app


app = create_application()
