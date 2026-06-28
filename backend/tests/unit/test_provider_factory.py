import pytest

from app.collector.providers.factory import create_provider
from app.collector.providers.whatsapp_web import WhatsAppWebProvider
from app.config.settings import Settings


def test_create_provider_returns_configured_provider() -> None:
    settings = Settings(WHATSAPP_PROVIDER="whatsapp_web", WHATSAPP_SESSION_PATH="/tmp/session")
    provider = create_provider(settings)
    assert isinstance(provider, WhatsAppWebProvider)


def test_create_provider_rejects_unknown_provider() -> None:
    settings = Settings(WHATSAPP_PROVIDER="not_a_real_provider")
    with pytest.raises(ValueError, match="Unknown WHATSAPP_PROVIDER"):
        create_provider(settings)
