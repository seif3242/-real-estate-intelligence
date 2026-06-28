from datetime import UTC, datetime

import pytest

from app.collector.providers.base import (
    CollectedAttachment,
    CollectedContentType,
    CollectedMessage,
    WhatsAppProvider,
)
from app.collector.service import CollectorService


class FakeProvider(WhatsAppProvider):
    """In-memory WhatsAppProvider used to test CollectorService without Playwright."""

    def __init__(self) -> None:
        self.connected = False
        self.session_checks = 0
        self.messages: list[CollectedMessage] = []

    async def connect(self) -> None:
        self.connected = True

    async def is_connected(self) -> bool:
        return self.connected

    async def maintain_session(self) -> None:
        self.session_checks += 1

    async def read_new_messages(self) -> list[CollectedMessage]:
        return self.messages

    async def download_attachment(
        self, message: CollectedMessage, attachment: CollectedAttachment
    ) -> bytes:
        return b""

    async def disconnect(self) -> None:
        self.connected = False


_FIXED_RECEIVED_AT = datetime(2024, 1, 1, tzinfo=UTC)


def _sample_message() -> CollectedMessage:
    return CollectedMessage(
        external_message_id="msg-1",
        group_external_id="group-1",
        group_name="Test Group",
        content_type=CollectedContentType.TEXT,
        text="hello",
        received_at=_FIXED_RECEIVED_AT,
    )


@pytest.mark.asyncio
async def test_start_connects_provider() -> None:
    provider = FakeProvider()
    service = CollectorService(provider)

    await service.start()

    assert provider.connected is True


@pytest.mark.asyncio
async def test_stop_disconnects_provider() -> None:
    provider = FakeProvider()
    service = CollectorService(provider)
    await service.start()

    await service.stop()

    assert provider.connected is False


@pytest.mark.asyncio
async def test_poll_once_returns_provider_messages() -> None:
    provider = FakeProvider()
    provider.messages = [_sample_message()]
    service = CollectorService(provider)

    messages = await service.poll_once()

    assert messages == [_sample_message()]
    assert provider.session_checks == 1


def test_whatsapp_provider_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        WhatsAppProvider()  # type: ignore[abstract]
