"""WhatsApp_Groups entity: maps a WhatsApp group to a developer (PRD §8.1)."""

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class WhatsAppGroup(Base, TimestampMixin):
    """A monitored WhatsApp group.

    A group must be explicitly onboarded (developer_id set) before its
    messages are classified/extracted; until then messages are stored raw
    only (System Design §6.1).
    """

    __tablename__ = "whatsapp_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_external_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    developer_id: Mapped[int | None] = mapped_column(
        ForeignKey("developers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_ignored: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarded_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(nullable=True)
