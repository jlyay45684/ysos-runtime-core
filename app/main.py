from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Demo API for orchestrating simple AI runtime workflows.",
    )
    app.include_router(router, prefix="/api")
    return app


app = create_app()
