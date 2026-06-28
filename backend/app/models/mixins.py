"""Shared column mixins for structured-extraction tables.

Launches, Requests, and Offers all derive from a Message and an Extraction,
and must follow the same FK-lifecycle rule: nullable FKs with ON DELETE SET
NULL back to Messages (never CASCADE), plus denormalized snapshot fields so
display context survives the 30-day raw-message purge (Engineering Rules
§7.2).
"""

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column


class StructuredExtractionMixin:
    """Common columns for permanent records derived from a classified message."""

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
    confidence_score: Mapped[float | None] = mapped_column(Numeric(4, 3), nullable=True)
