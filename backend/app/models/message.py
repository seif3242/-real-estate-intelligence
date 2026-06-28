"""Raw WhatsApp message. Purged automatically after 30 days (PRD §13)."""

from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin
from app.models.enums import MessageContentType


class Message(Base, TimestampMixin):
    """A raw collected WhatsApp message.

    This table is subject to a 30-day retention purge job (not implemented
    in Milestone 1). Permanent tables that reference this row must use a
    nullable FK with ON DELETE SET NULL — never CASCADE (Engineering Rules
    §7.2) — and store a denormalized snapshot of any display fields.
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    whatsapp_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("whatsapp_groups.id", ondelete="SET NULL"), nullable=True, index=True
    )
    external_message_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    content_type: Mapped[MessageContentType] = mapped_column(
        Enum(MessageContentType, name="message_content_type"), nullable=False
    )
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
