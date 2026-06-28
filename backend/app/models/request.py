"""Request entity (PRD §6) — a buyer/agent request seen in a group."""

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin
from app.models.mixins import StructuredExtractionMixin


class Request(Base, TimestampMixin, StructuredExtractionMixin):
    """A request for a unit/project. Permanent record."""

    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_information: Mapped[str | None] = mapped_column(Text, nullable=True)
