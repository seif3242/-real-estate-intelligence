"""Playwright-driven WhatsApp Web adapter.

Milestone 2 scope: real connection lifecycle only — open WhatsApp Web,
support first-time QR authentication, persist the session so restarts
reuse it, verify whether a session is still valid, and list group chat
names. Actually opening a group, reading its messages, and downloading
attachments are deliberately not implemented yet (see
docs/WHATSAPP_AUTHENTICATION.md and System Design §2.2).

Selectors below target WhatsApp Web's current DOM and may need updating if
WhatsApp changes its markup; they are kept as module-level constants for
that reason.
"""

import logging
import time
from collections.abc import Iterable
from pathlib import Path

from playwright.async_api import BrowserContext, Page, Playwright, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from app.collector.providers.base import (
    CollectedAttachment,
    CollectedMessage,
    WhatsAppProvider,
)
from app.collector.providers.exceptions import ConnectionLostError, QrLoginTimeoutError

logger = logging.getLogger(__name__)

WHATSAPP_WEB_URL = "https://web.whatsapp.com"

# WhatsApp Web renders the QR code inside this container while logged out.
QR_CODE_SELECTOR = "div[data-testid='qrcode']"
# Present only once a session is authenticated; used to confirm login state.
CHAT_LIST_SELECTOR = "div[aria-label='Chat list']"
CHAT_ROW_SELECTOR = "div[aria-label='Chat list'] div[role='listitem']"

# Icon shown for chats without a custom photo. Groups with a custom photo are
# not detected by this heuristic — see docs/WHATSAPP_AUTHENTICATION.md.
_GROUP_ICON_NAMES = frozenset({"default-group", "default-group-refreshed"})

SESSION_CHECK_TIMEOUT_MS = 5_000
QR_LOGIN_TIMEOUT_SECONDS = 120.0
LOGIN_POLL_INTERVAL_MS = 3_000


def _is_group_row(icon_names: Iterable[str]) -> bool:
    """Pure helper so the group-detection heuristic is unit-testable without Playwright."""
    return any(name in _GROUP_ICON_NAMES for name in icon_names)


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
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def connect(self) -> None:
        if self._context is not None:
            return
        self._session_path.mkdir(parents=True, exist_ok=True)
        self._playwright = await async_playwright().start()
        self._context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self._session_path),
            headless=True,
        )
        self._page = (
            self._context.pages[0] if self._context.pages else await self._context.new_page()
        )
        await self._page.goto(WHATSAPP_WEB_URL)

        if await self._wait_for_logged_in(timeout_ms=SESSION_CHECK_TIMEOUT_MS):
            logger.info(
                "WhatsApp Web connected using persisted session (session=%s)", self._session_path
            )
            return

        await self._authenticate_via_qr()
        logger.info(
            "WhatsApp Web connected after QR authentication (session=%s)", self._session_path
        )

    async def _wait_for_logged_in(self, timeout_ms: int) -> bool:
        assert self._page is not None
        try:
            await self._page.wait_for_selector(CHAT_LIST_SELECTOR, timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    async def _authenticate_via_qr(self) -> None:
        assert self._page is not None
        qr_path = self._session_path / "qr.png"
        deadline = time.monotonic() + QR_LOGIN_TIMEOUT_SECONDS

        while time.monotonic() < deadline:
            qr_element = await self._page.query_selector(QR_CODE_SELECTOR)
            if qr_element is not None:
                await qr_element.screenshot(path=str(qr_path))
                logger.info(
                    "Scan the QR code at %s with WhatsApp > Linked Devices within %.0fs "
                    "to authenticate.",
                    qr_path,
                    deadline - time.monotonic(),
                )
            if await self._wait_for_logged_in(timeout_ms=LOGIN_POLL_INTERVAL_MS):
                return

        raise QrLoginTimeoutError(
            f"QR code was not scanned within {QR_LOGIN_TIMEOUT_SECONDS:.0f}s. "
            f"Re-run the authentication flow and scan the QR code saved at {qr_path}."
        )

    async def is_connected(self) -> bool:
        if self._context is None or self._page is None:
            return False
        return await self._wait_for_logged_in(timeout_ms=SESSION_CHECK_TIMEOUT_MS)

    async def maintain_session(self) -> None:
        if not await self.is_connected():
            raise ConnectionLostError("WhatsApp Web session is not connected or not logged in.")

    async def list_groups(self) -> list[str]:
        if not await self.is_connected():
            raise ConnectionLostError("Cannot list groups: provider is not connected.")
        assert self._page is not None

        names: list[str] = []
        for row in await self._page.query_selector_all(CHAT_ROW_SELECTOR):
            icon_elements = await row.query_selector_all("span[data-icon]")
            icon_names = [
                name
                for icon in icon_elements
                if (name := await icon.get_attribute("data-icon")) is not None
            ]
            if not _is_group_row(icon_names):
                continue

            title_element = await row.query_selector("span[title]")
            if title_element is None:
                continue
            title = await title_element.get_attribute("title")
            if title:
                names.append(title)
        return names

    async def read_new_messages(self) -> list[CollectedMessage]:
        raise NotImplementedError(
            "Reading WhatsApp messages is not implemented in Milestone 2."
        )

    async def download_attachment(
        self, message: CollectedMessage, attachment: CollectedAttachment
    ) -> bytes:
        raise NotImplementedError(
            "WhatsApp attachment download is not implemented in Milestone 2."
        )

    async def disconnect(self) -> None:
        if self._context is not None:
            await self._context.close()
            self._context = None
        self._page = None
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None
        logger.info("WhatsApp Web provider disconnected")
