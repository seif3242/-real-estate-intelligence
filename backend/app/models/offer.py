"""Offer entity (PRD §6)."""

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin
from app.models.mixins import StructuredExtractionMixin


class Offer(Base, TimestampMixin, StructuredExtractionMixin):
    """A unit/project offer. Permanent record."""

    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    offer_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    down_payment: Mapped[str | None] = mapped_column(Text, nullable=True)
    installments: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_information: Mapped[str | None] = mapped_column(Text, nullable=True)
