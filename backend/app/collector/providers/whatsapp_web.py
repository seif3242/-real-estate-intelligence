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

Group detection and message reading do not use the DOM at all (see
`_GROUP_LOOKUP_SCRIPT` and `_READ_MESSAGES_SCRIPT`): both locate WhatsApp
Web's internal webpack module store and read its data model directly —
chat type via `id.server`, message content via the chat's own message
collection — which is unaffected by rendering details like custom photos
or RTL/Arabic text shaping. See docs/WHATSAPP_AUTHENTICATION.md for the
rationale and its limitations.
"""

import logging
import time
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import BrowserContext, Page, Playwright, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from app.collector.providers.base import (
    DEFAULT_MESSAGE_READ_LIMIT,
    CollectedAttachment,
    CollectedContentType,
    CollectedMessage,
    ExtractedMessage,
    WhatsAppProvider,
)
from app.collector.providers.exceptions import (
    ConnectionLostError,
    GroupListingUnavailableError,
    GroupNotFoundError,
    QrLoginTimeoutError,
)

logger = logging.getLogger(__name__)

WHATSAPP_WEB_URL = "https://web.whatsapp.com"

# WhatsApp Web renders the QR code inside this container while logged out.
QR_CODE_SELECTOR = "div[data-testid='qrcode']"
# Present only once a session is authenticated; used to confirm login state.
CHAT_LIST_SELECTOR = "div[aria-label='Chat list']"

SESSION_CHECK_TIMEOUT_MS = 5_000
QR_LOGIN_TIMEOUT_SECONDS = 120.0
LOGIN_POLL_INTERVAL_MS = 3_000

# Locates WhatsApp Web's internal webpack module store and reads the chat
# collection directly, rather than inferring chat type from rendered DOM/icons.
# Pushing a synthetic chunk onto the page's own `webpackChunk*` array hands us
# a working `require`, which we use to find the module exporting `Chat` (with
# `getModelsArray()`). Each chat's `id.server` is `"g.us"` for groups and
# `"c.us"`/`"s.whatsapp.net"` for individuals — this comes from WhatsApp's own
# data model, so it is correct regardless of custom photos. Returns `None` if
# the store can't be located (e.g. WhatsApp changed its bundling), which the
# caller must treat as a hard failure, never as "zero groups".
_GROUP_LOOKUP_SCRIPT = """
() => {
    const chunkKey = Object.keys(window).find((key) => key.startsWith("webpackChunk"));
    if (!chunkKey) {
        return null;
    }

    let webpackRequire;
    window[chunkKey].push([
        [Symbol("collector-group-lookup")],
        {},
        (require) => { webpackRequire = require; },
    ]);
    if (!webpackRequire) {
        return null;
    }

    let chatCollection = null;
    for (const moduleId of Object.keys(webpackRequire.m)) {
        let moduleExports;
        try {
            moduleExports = webpackRequire(moduleId);
        } catch (_error) {
            continue;
        }
        const candidate = moduleExports && moduleExports.default;
        if (candidate && candidate.Chat && typeof candidate.Chat.getModelsArray === "function") {
            chatCollection = candidate.Chat;
            break;
        }
    }
    if (!chatCollection) {
        return null;
    }

    return chatCollection
        .getModelsArray()
        .filter((chat) => chat.id && chat.id.server === "g.us")
        .map((chat) => chat.formattedTitle || chat.name || (chat.id && chat.id.user) || "");
}
"""

# Locates the named group via the same webpack module store as
# `_GROUP_LOOKUP_SCRIPT`, then reads its `limit` most recent messages from
# the chat's own message collection (`chat.msgs`) rather than scraping
# message bubbles from the DOM. This is deliberate: bubble markup/RTL
# shaping for Arabic text is exactly the kind of rendering detail that made
# the old icon-based group heuristic unreliable, whereas the underlying
# message objects (sender, timestamp, body, MIME type) are plain Unicode
# data independent of how WhatsApp Web chooses to render them.
#
# Returns one of:
#   {"error": "store_unavailable"}  — webpack store couldn't be located.
#   {"error": "group_not_found"}    — no group matched `groupName`.
#   {"messages": [...]}             — oldest message first, newest last.
_READ_MESSAGES_SCRIPT = """
async ({ groupName, limit }) => {
    const chunkKey = Object.keys(window).find((key) => key.startsWith("webpackChunk"));
    if (!chunkKey) {
        return { error: "store_unavailable" };
    }

    let webpackRequire;
    window[chunkKey].push([
        [Symbol("collector-message-read")],
        {},
        (require) => { webpackRequire = require; },
    ]);
    if (!webpackRequire) {
        return { error: "store_unavailable" };
    }

    let chatCollection = null;
    for (const moduleId of Object.keys(webpackRequire.m)) {
        let moduleExports;
        try {
            moduleExports = webpackRequire(moduleId);
        } catch (_error) {
            continue;
        }
        const candidate = moduleExports && moduleExports.default;
        if (candidate && candidate.Chat && typeof candidate.Chat.getModelsArray === "function") {
            chatCollection = candidate.Chat;
            break;
        }
    }
    if (!chatCollection) {
        return { error: "store_unavailable" };
    }

    const chat = chatCollection
        .getModelsArray()
        .find(
            (candidate) =>
                candidate.id &&
                candidate.id.server === "g.us" &&
                (candidate.formattedTitle === groupName || candidate.name === groupName)
        );
    if (!chat || !chat.msgs || typeof chat.msgs.getModelsArray !== "function") {
        return { error: "group_not_found" };
    }

    // Mirrors a user opening the chat, which is what causes WhatsApp Web to
    // sync its message history into `chat.msgs` in the first place.
    try {
        if (typeof chat.setActive === "function") {
            chat.setActive(true);
        }
    } catch (_error) {
        // Best effort: fall through and read whatever is already loaded.
    }

    // Pull in older messages (WhatsApp Web's own "load earlier messages"
    // mechanism) until enough are available, the chat is exhausted, or we
    // give up after a bounded number of attempts.
    try {
        for (let attempt = 0; attempt < 20; attempt += 1) {
            if (chat.msgs.getModelsArray().length >= limit) {
                break;
            }
            if (typeof chat.loadEarlierMsgs !== "function") {
                break;
            }
            const before = chat.msgs.getModelsArray().length;
            await chat.loadEarlierMsgs();
            if (chat.msgs.getModelsArray().length <= before) {
                break;
            }
        }
    } catch (_error) {
        // Best effort: return whatever was already loaded.
    }

    const all = chat.msgs.getModelsArray();
    const recent = all.slice(Math.max(0, all.length - limit));

    return {
        messages: recent.map((msg) => {
            const senderObj = msg.senderObj;
            const senderName =
                (senderObj && (senderObj.pushname || senderObj.formattedName || senderObj.name)) ||
                (msg.author ? msg.author.split("@")[0] : null) ||
                null;

            const isText = msg.type === "chat";
            const isPdf = msg.type === "document" && msg.mimetype === "application/pdf";

            return {
                sender_name: senderName,
                timestamp: typeof msg.t === "number" ? msg.t * 1000 : null,
                message_type: isText ? "text" : isPdf ? "pdf" : "unsupported",
                message_text: isText ? msg.body || null : null,
                pdf_file_name: isPdf ? msg.filename || null : null,
            };
        }),
    };
}
"""


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

        result = await self._page.evaluate(_GROUP_LOOKUP_SCRIPT)
        if result is None:
            raise GroupListingUnavailableError(
                "Could not locate WhatsApp Web's internal chat store; group names "
                "cannot be reliably listed. This usually means WhatsApp Web has "
                "changed its internal module bundling — see "
                "docs/WHATSAPP_AUTHENTICATION.md for the known limitation and the "
                "recommended long-term fix (the official WhatsApp Business Platform API)."
            )
        return [name for name in result if name]

    async def read_new_messages(self) -> list[CollectedMessage]:
        raise NotImplementedError("Reading WhatsApp messages is not implemented in Milestone 2.")

    async def read_recent_messages(
        self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
    ) -> list[ExtractedMessage]:
        if not await self.is_connected():
            raise ConnectionLostError("Cannot read messages: provider is not connected.")
        assert self._page is not None

        result = await self._page.evaluate(
            _READ_MESSAGES_SCRIPT, {"groupName": group_name, "limit": limit}
        )
        if result.get("error") == "store_unavailable":
            raise GroupListingUnavailableError(
                "Could not locate WhatsApp Web's internal chat store; messages "
                "cannot be reliably read. This usually means WhatsApp Web has "
                "changed its internal module bundling — see "
                "docs/WHATSAPP_AUTHENTICATION.md for the known limitation and the "
                "recommended long-term fix (the official WhatsApp Business Platform API)."
            )
        if result.get("error") == "group_not_found":
            raise GroupNotFoundError(
                f"No group named {group_name!r} is visible to the connected account."
            )

        return [
            ExtractedMessage(
                sender_name=msg["sender_name"],
                timestamp=(
                    datetime.fromtimestamp(msg["timestamp"] / 1000, tz=UTC)
                    if msg["timestamp"] is not None
                    else None
                ),
                message_type=CollectedContentType(msg["message_type"]),
                message_text=msg["message_text"],
                pdf_file_name=msg["pdf_file_name"],
            )
            for msg in result["messages"]
        ]

    async def download_attachment(
        self, message: CollectedMessage, attachment: CollectedAttachment
    ) -> bytes:
        raise NotImplementedError("WhatsApp attachment download is not implemented in Milestone 2.")

    async def disconnect(self) -> None:
        if self._context is not None:
            await self._context.close()
            self._context = None
        self._page = None
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None
        logger.info("WhatsApp Web provider disconnected")
