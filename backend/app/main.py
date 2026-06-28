"""FastAPI application entrypoint.

Milestone 2 scope: app factory + health check + collector group listing.
Dashboard, Chat, Notifications, and onboarding endpoints are added in
later milestones.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.collector import router as collector_router
from app.api.health import router as health_router
from app.config.logging import configure_logging
from app.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(collector_router)
    return app


app = create_app()
