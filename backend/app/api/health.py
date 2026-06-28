"""Health check endpoint, used by Docker healthchecks (Engineering Rules §20)."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
