"""Manual correction audit trail for AI extractions (PRD §7.2)."""

from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ExtractionCorrection(Base, TimestampMixin):
    """A user-made correction to a single field of an Extraction.

    Stored separately from the original AI output so both the AI's answer
    and the user's correction remain available. A later re-processing pass
    of the same content must not overwrite a field that has a correction
    on record (Engineering Rules §7.5).
    """

    __tablename__ = "extraction_corrections"

    id: Mapped[int] = mapped_column(primary_key=True)
    extraction_id: Mapped[int] = mapped_column(
        ForeignKey("extractions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    original_ai_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    corrected_value: Mapped[str] = mapped_column(Text, nullable=False)
    corrected_at: Mapped[datetime] = mapped_column(nullable=False)
