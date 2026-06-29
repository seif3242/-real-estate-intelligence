"""Collector endpoints. Milestone 3 scope: group listing and on-demand
message reading for a single group — no Dashboard, no background sync
(System Design §2.2)."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.collector.providers.base import DEFAULT_MESSAGE_READ_LIMIT, ExtractedMessage
from app.collector.providers.exceptions import GroupNotFoundError, ProviderError
from app.collector.providers.factory import create_provider
from app.collector.service import CollectorService
from app.config.settings import Settings, get_settings

router = APIRouter(prefix="/collector", tags=["collector"])

MAX_MESSAGE_READ_LIMIT = 500


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


@router.get("/messages", response_model=list[ExtractedMessage])
async def read_recent_messages(
    group_name: str = Query(..., min_length=1),
    limit: int = Query(default=DEFAULT_MESSAGE_READ_LIMIT, ge=1, le=MAX_MESSAGE_READ_LIMIT),
    service: CollectorService = Depends(get_collector_service),
) -> list[ExtractedMessage]:
    await service.start()
    try:
        return await service.read_recent_messages(group_name, limit)
    except GroupNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        await service.stop()
