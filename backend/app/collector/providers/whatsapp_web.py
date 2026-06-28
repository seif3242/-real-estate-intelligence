"""Playwright-driven WhatsApp Web adapter.

Milestone 1 scope: structural skeleton only. Session bootstrap and the
actual message/attachment scraping logic are deliberately not implemented
yet (no real WhatsApp synchronization in this milestone) — methods either
manage the Playwright browser lifecycle or raise NotImplementedError where
real scraping logic will land in a later milestone.
"""

import logging
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Playwright, async_playwright

from app.collector.providers.base import (
    CollectedAttachment,
    CollectedMessage,
    WhatsAppProvider,
)
from app.collector.providers.exceptions import ConnectionLostError

logger = logging.getLogger(__name__)

WHATSAPP_WEB_URL = "https://web.whatsapp.com"


class WhatsAppWebProvider(WhatsAppProvider):
    """WhatsAppProvider implementation backed by Playwright + WhatsApp Web.

    The browser session profile is persisted under `session_path` so login
    survives restarts (Engineering Rules §8: "Collector stores session
    securely"). Encryption of that directory at rest is an operational
    concern handled outside this class (e.g. an encrypted volume).
    """

    def __init__(self, session_path: str) -> None:
        self._session_path = Path(session_path)
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    async def connect(self) -> None:
        if self._context is not None:
            return
        self._session_path.mkdir(parents=True, exist_ok=True)
        self._playwright = await async_playwright().start()
        self._context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self._session_path),
            headless=True,
        )
        logger.info("WhatsApp Web provider connected (session=%s)", self._session_path)

    async def is_connected(self) -> bool:
        return self._context is not None

    async def maintain_session(self) -> None:
        if self._context is None:
            raise ConnectionLostError("Provider is not connected; call connect() first.")
        # Real session-health checking and reconnect/backoff logic is
        # implemented in a later milestone, alongside actual message sync.

    async def read_new_messages(self) -> list[CollectedMessage]:
        raise NotImplementedError(
            "WhatsApp message synchronization is not implemented in Milestone 1."
        )

    async def download_attachment(
        self, message: CollectedMessage, attachment: CollectedAttachment
    ) -> bytes:
        raise NotImplementedError(
            "WhatsApp attachment download is not implemented in Milestone 1."
        )

    async def disconnect(self) -> None:
        if self._context is not None:
            await self._context.close()
            self._context = None
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None
        logger.info("WhatsApp Web provider disconnected")
