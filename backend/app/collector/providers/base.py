"""WhatsApp Provider Interface (System Design §2.2 / Engineering Rules §8.5).

This is the only contract the rest of the system (Queue, Parser, etc.) may
depend on. The current implementation (whatsapp_web.py) is a Playwright
adapter; a future provider (e.g. the official WhatsApp Business Cloud API)
can be swapped in by implementing this same interface, with no changes
required anywhere else in the system.

No business logic, classification, or extraction belongs here or in any
implementation of this interface (Engineering Rules §2) — it only collects
raw content and hands it off.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CollectedContentType(StrEnum):
    """Content type of a collected message, as seen by the Collector.

    V1 only forwards TEXT and PDF for downstream processing; UNSUPPORTED
    (image/voice/video) is recorded but never analyzed (PRD §5).
    """

    TEXT = "text"
    PDF = "pdf"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class CollectedAttachment:
    """A file attachment discovered on a message, before download."""

    external_attachment_id: str
    content_type: CollectedContentType
    file_name: str


@dataclass(frozen=True, slots=True)
class CollectedMessage:
    """A single message as read from WhatsApp, with no interpretation applied."""

    external_message_id: str
    group_external_id: str
    group_name: str
    content_type: CollectedContentType
    text: str | None
    received_at: datetime
    attachments: tuple[CollectedAttachment, ...] = ()


DEFAULT_MESSAGE_READ_LIMIT = 50


@dataclass(frozen=True, slots=True)
class ExtractedMessage:
    """A single message read from a specific group, for on-demand inspection.

    Deliberately narrower than `CollectedMessage`: only the fields a human
    reviewer needs (Milestone 3 scope), no message id, group id, or content
    hash — those belong to the future sync/dedup pipeline, not this one-shot
    read.
    """

    sender_name: str | None
    timestamp: datetime | None
    message_type: CollectedContentType
    message_text: str | None
    pdf_file_name: str | None


class WhatsAppProvider(ABC):
    """Abstract contract for any WhatsApp transport (Web automation, official API, etc.)."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish or restore a session. Must be safe to call repeatedly (idempotent)."""

    @abstractmethod
    async def is_connected(self) -> bool:
        """Return whether the provider currently has a usable, authenticated session."""

    @abstractmethod
    async def maintain_session(self) -> None:
        """Keep the session alive; perform reconnect/backoff if the connection was lost."""

    @abstractmethod
    async def list_groups(self) -> list[str]:
        """Return the names of all groups visible to the connected account. Read-only
        discovery only — does not open a group or read any of its messages."""

    @abstractmethod
    async def read_new_messages(self) -> list[CollectedMessage]:
        """Return messages received since the last checkpoint. Read-only; never marks
        messages as read/replied, edits, or deletes anything (Engineering Rules §8)."""

    @abstractmethod
    async def read_recent_messages(
        self, group_name: str, limit: int = DEFAULT_MESSAGE_READ_LIMIT
    ) -> list[ExtractedMessage]:
        """Open the named group and return its `limit` most recent messages, oldest
        first. Read-only discovery only — no database writes, deduplication, content
        hashing, or attachment download; PDF attachments are identified by file name
        only, never downloaded or analyzed."""

    @abstractmethod
    async def download_attachment(
        self, message: CollectedMessage, attachment: CollectedAttachment
    ) -> bytes:
        """Download a single attachment's raw bytes. Only TEXT/PDF content types are
        expected to be downloaded in V1; callers must not request UNSUPPORTED content."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Release any resources held by the provider (e.g. close the browser)."""
