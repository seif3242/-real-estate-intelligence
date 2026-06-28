"""Commission_History entity (PRD §12) — append-only, never overwritten."""

from datetime import date

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class CommissionHistory(Base, TimestampMixin):
    """A single commission-change event for a project. Rows are never updated/overwritten."""

    __tablename__ = "commission_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"), nullable=True, index=True
    )
    project_name_snapshot: Mapped[str | None] = mapped_column(String(255), nullable=True)
    commission_value: Mapped[str] = mapped_column(Text, nullable=False)
    changed_on: Mapped[date] = mapped_column(nullable=False, index=True)
