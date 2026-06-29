from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.api.collector import get_collector_service
from app.collector.providers.base import (
    DEFAULT_MESSAGE_READ_LIMIT,
    CollectedContentType,
    CollectedMessage,
    ExtractedMessage,
    WhatsAppProvider,
)
from app.collector.providers.exceptions import GroupNotFoundError, QrLoginTimeoutError
from app.collector.service import CollectorService
from app.main import app


class FakeProvider(WhatsAppProvider):
    """In-memory WhatsAppProvider used to test the /collector endpoints."""

    def __init__(self) -> None:
        self.connected = False
        self.groups: list[str] = []
        self.recent_messages: list[ExtractedMessage] = []

    async def connect(self) -> None:
        self.connected = True

    async def is_connected(self) -> bool:
        return self.connected

    async def maintain_session(self) -> None:
        pass

    async def list_groups(self) -> list[str]:
        return self.groups

    async def read_new_messages(self) -> list[CollectedMessage]:
        return []

    async def read_recent_messages(
        self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
    ) -> list[ExtractedMessage]:
        return self.recent_messages

    async def download_attachment(self, message: CollectedMessage, attachment: object) -> bytes:
        return b""

    async def disconnect(self) -> None:
        self.connected = False


def test_list_groups_endpoint_returns_group_names() -> None:
    provider = FakeProvider()
    provider.groups = ["Group A", "Group B"]
    app.dependency_overrides[get_collector_service] = lambda: CollectorService(provider)
    client = TestClient(app)

    try:
        response = client.get("/collector/groups")
    finally:
        app.dependency_overrides.pop(get_collector_service, None)

    assert response.status_code == 200
    assert response.json() == ["Group A", "Group B"]
    assert provider.connected is False  # service.stop() ran after the request


def test_list_groups_endpoint_returns_503_on_provider_error() -> None:
    class FailingProvider(FakeProvider):
        async def list_groups(self) -> list[str]:
            raise QrLoginTimeoutError("QR code was not scanned in time.")

    app.dependency_overrides[get_collector_service] = lambda: CollectorService(FailingProvider())
    client = TestClient(app)

    try:
        response = client.get("/collector/groups")
    finally:
        app.dependency_overrides.pop(get_collector_service, None)

    assert response.status_code == 503


def test_read_messages_endpoint_returns_extracted_messages() -> None:
    provider = FakeProvider()
    provider.recent_messages = [
        ExtractedMessage(
            sender_name="سارة",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
            message_type=CollectedContentType.TEXT,
            message_text="مرحبا",
            pdf_file_name=None,
        ),
        ExtractedMessage(
            sender_name="John",
            timestamp=datetime(2024, 1, 2, tzinfo=UTC),
            message_type=CollectedContentType.PDF,
            message_text=None,
            pdf_file_name="brochure.pdf",
        ),
    ]
    app.dependency_overrides[get_collector_service] = lambda: CollectorService(provider)
    client = TestClient(app)

    try:
        response = client.get("/collector/messages", params={"group_name": "Test Group"})
    finally:
        app.dependency_overrides.pop(get_collector_service, None)

    assert response.status_code == 200
    body = response.json()
    assert body[0]["sender_name"] == "سارة"
    assert body[0]["message_type"] == "text"
    assert body[0]["message_text"] == "مرحبا"
    assert body[1]["message_type"] == "pdf"
    assert body[1]["pdf_file_name"] == "brochure.pdf"


def test_read_messages_endpoint_returns_404_when_group_not_found() -> None:
    class FailingProvider(FakeProvider):
        async def read_recent_messages(
            self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
        ) -> list[ExtractedMessage]:
            raise GroupNotFoundError(f"No group named {group_name!r} is visible.")

    app.dependency_overrides[get_collector_service] = lambda: CollectorService(FailingProvider())
    client = TestClient(app)

    try:
        response = client.get("/collector/messages", params={"group_name": "Missing"})
    finally:
        app.dependency_overrides.pop(get_collector_service, None)

    assert response.status_code == 404


def test_read_messages_endpoint_returns_503_on_provider_error() -> None:
    class FailingProvider(FakeProvider):
        async def read_recent_messages(
            self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
        ) -> list[ExtractedMessage]:
            raise QrLoginTimeoutError("QR code was not scanned in time.")

    app.dependency_overrides[get_collector_service] = lambda: CollectorService(FailingProvider())
    client = TestClient(app)

    try:
        response = client.get("/collector/messages", params={"group_name": "Test Group"})
    finally:
        app.dependency_overrides.pop(get_collector_service, None)

    assert response.status_code == 503
