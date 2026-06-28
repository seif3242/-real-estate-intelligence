"""Notification entity. Delivered via Dashboard only in V1 (PRD §19.1)."""

from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    """An in-app notification (daily summary, launch/price/commission alert)."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(nullable=True)
