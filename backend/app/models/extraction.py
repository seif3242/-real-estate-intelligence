"""AI extraction result. Permanent record, even after the source Message expires."""

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin
from app.models.enums import MessageClassification


class Extraction(Base, TimestampMixin):
    """Result of running the AI Parser/PDF Processor on a piece of content.

    Linked to the source Message via a nullable FK (SET NULL on delete) so
    the extraction survives the 30-day raw-message purge (Engineering Rules
    §7.2). content_hash drives the pre-AI duplicate-detection step (PRD §10
    / System Design §3.1): a new Message matching an existing content_hash
    reuses this row instead of triggering another AI call.
    """

    __tablename__ = "extractions"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"), nullable=True, index=True
    )
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    classification: Mapped[MessageClassification] = mapped_column(
        Enum(MessageClassification, name="message_classification"), nullable=False
    )
    confidence_score: Mapped[float] = mapped_column(Numeric(4, 3), nullable=False)
    raw_ai_output: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
