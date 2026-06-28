"""Provider factory — selects a WhatsAppProvider implementation by configuration.

This is the single place that knows about concrete provider classes; adding
a future provider (e.g. an official Business API adapter) only requires
registering it here, per Engineering Rules §8.5.
"""

from app.collector.providers.base import WhatsAppProvider
from app.collector.providers.whatsapp_web import WhatsAppWebProvider
from app.config.settings import Settings

_PROVIDERS = {
    "whatsapp_web": WhatsAppWebProvider,
}


def create_provider(settings: Settings) -> WhatsAppProvider:
    """Instantiate the configured WhatsAppProvider."""
    try:
        provider_cls = _PROVIDERS[settings.whatsapp_provider]
    except KeyError as exc:
        raise ValueError(f"Unknown WHATSAPP_PROVIDER: {settings.whatsapp_provider!r}") from exc
    return provider_cls(session_path=settings.whatsapp_session_path)
