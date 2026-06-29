"""WhatsApp Collector service.

Owns a single WhatsAppProvider instance and its connect/disconnect
lifecycle. Forwarding collected messages into the Message Processing Queue
is not implemented in Milestone 1 (the Queue does not exist yet) — this
service intentionally stops at "read messages from the provider."
"""

import logging

from app.collector.providers.base import (
    DEFAULT_MESSAGE_READ_LIMIT,
    CollectedMessage,
    ExtractedMessage,
    WhatsAppProvider,
)

logger = logging.getLogger(__name__)


class CollectorService:
    """Coordinates a WhatsAppProvider. Contains no AI/classification logic."""

    def __init__(self, provider: WhatsAppProvider) -> None:
        self._provider = provider

    async def start(self) -> None:
        await self._provider.connect()
        logger.info("Collector started")

    async def stop(self) -> None:
        await self._provider.disconnect()
        logger.info("Collector stopped")

    async def poll_once(self) -> list[CollectedMessage]:
        """Read and return any new messages. Handoff to a processing queue is
        added in a later milestone."""
        await self._provider.maintain_session()
        return await self._provider.read_new_messages()

    async def list_groups(self) -> list[str]:
        """Return the names of all groups visible to the connected account."""
        await self._provider.maintain_session()
        return await self._provider.list_groups()

    async def read_recent_messages(
        self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
    ) -> list[ExtractedMessage]:
        """Open the named group and return its most recent messages."""
        await self._provider.maintain_session()
        return await self._provider.read_recent_messages(group_name, limit)
