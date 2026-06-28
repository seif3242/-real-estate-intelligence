"""Application-wide logging configuration."""

import logging
import sys

from app.config.settings import get_settings


def configure_logging() -> None:
    """Configure root logging handlers and level from settings.

    Must be called once at application startup (see app.main).
    """
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
