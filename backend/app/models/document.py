"""PDF document entity. Permanent record (PRD §9)."""

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    """A PDF downloaded from WhatsApp, linked to a project/developer.

    message_id is nullable with ON DELETE SET NULL so the document survives
    the 30-day raw-message purge; project/developer names are snapshotted
    for display continuity (Engineering Rules §7.2).
    """

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"), nullable=True, index=True
    )
    extraction_id: Mapped[int | None] = mapped_column(
        ForeignKey("extractions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True
    )
    developer_id: Mapped[int | None] = mapped_column(
        ForeignKey("developers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    project_name_snapshot: Mapped[str | None] = mapped_column(String(255), nullable=True)
    developer_name_snapshot: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(4, 3), nullable=True)
