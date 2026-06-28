"""Collector endpoints. Milestone 2 scope: group listing only — no message
reading, no Dashboard, no background sync (System Design §2.2)."""

from fastapi import APIRouter, Depends, HTTPException

from app.collector.providers.exceptions import ProviderError
from app.collector.providers.factory import create_provider
from app.collector.service import CollectorService
from app.config.settings import Settings, get_settings

router = APIRouter(prefix="/collector", tags=["collector"])


def get_collector_service(settings: Settings = Depends(get_settings)) -> CollectorService:
    return CollectorService(create_provider(settings))


@router.get("/groups", response_model=list[str])
async def list_groups(
    service: CollectorService = Depends(get_collector_service),
) -> list[str]:
    await service.start()
    try:
        return await service.list_groups()
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        await service.stop()
