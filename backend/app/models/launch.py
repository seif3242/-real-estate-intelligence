"""Launch entity (PRD §6)."""

from datetime import date

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin
from app.models.mixins import StructuredExtractionMixin


class Launch(Base, TimestampMixin, StructuredExtractionMixin):
    """A new project/unit launch announcement. Permanent record."""

    __tablename__ = "launches"

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_types: Mapped[str | None] = mapped_column(Text, nullable=True)
    starting_price: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_date: Mapped[date | None] = mapped_column(nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
