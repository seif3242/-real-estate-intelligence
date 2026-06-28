from fastapi.testclient import TestClient

from app.api.collector import get_collector_service
from app.collector.providers.base import CollectedMessage, WhatsAppProvider
from app.collector.providers.exceptions import QrLoginTimeoutError
from app.collector.service import CollectorService
from app.main import app


class FakeProvider(WhatsAppProvider):
    """In-memory WhatsAppProvider used to test the /collector/groups endpoint."""

    def __init__(self) -> None:
        self.connected = False
        self.groups: list[str] = []

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
