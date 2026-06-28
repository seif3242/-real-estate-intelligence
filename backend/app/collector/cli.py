"""First-time WhatsApp Web authentication bootstrap.

Run this once (locally or via `docker compose exec backend python -m
app.collector.cli`) to scan the QR code and persist a session under
WHATSAPP_SESSION_PATH. See docs/WHATSAPP_AUTHENTICATION.md for the full
walkthrough. After this succeeds, the application reuses the saved session
automatically — this script does not need to be run again unless the
session is invalidated (e.g. unlinked from the phone).
"""

import asyncio
import logging

from app.collector.providers.factory import create_provider
from app.collector.service import CollectorService
from app.config.logging import configure_logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


async def main() -> None:
    configure_logging()
    settings = get_settings()
    service = CollectorService(create_provider(settings))

    await service.start()
    try:
        groups = await service.list_groups()
        logger.info("Authenticated. Found %d group(s):", len(groups))
        for name in groups:
            logger.info(" - %s", name)
    finally:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
