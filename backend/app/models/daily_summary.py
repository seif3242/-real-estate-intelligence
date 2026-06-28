"""Daily_Summaries entity (PRD §19) — permanent record."""

from datetime import date

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class DailySummary(Base, TimestampMixin):
    """A generated daily summary, one row per calendar day."""

    __tablename__ = "daily_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    summary_date: Mapped[date] = mapped_column(nullable=False, unique=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
