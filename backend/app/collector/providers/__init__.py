"""WhatsApp Provider abstraction and implementations."""

from app.collector.providers.base import (
    CollectedAttachment,
    CollectedContentType,
    CollectedMessage,
    WhatsAppProvider,
)
from app.collector.providers.factory import create_provider

__all__ = [
    "CollectedAttachment",
    "CollectedContentType",
    "CollectedMessage",
    "WhatsAppProvider",
    "create_provider",
]
