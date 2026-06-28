"""Shared enums for the data model.

MessageClassification is the unified taxonomy defined in PRD §6 / System
Design §4 and must stay identical across the PRD, System Design, and this
schema.
"""

import enum


class MessageContentType(enum.StrEnum):
    """Content types collected from WhatsApp. V1 only processes TEXT and PDF
    (PRD §5); UNSUPPORTED covers images/voice/video, stored raw but never
    classified/extracted in V1."""

    TEXT = "text"
    PDF = "pdf"
    UNSUPPORTED = "unsupported"


class MessageClassification(enum.StrEnum):
    """Unified message taxonomy (PRD §6 / System Design §4)."""

    LAUNCH = "launch"
    REQUEST = "request"
    OFFER = "offer"
    COMMISSION_UPDATE = "commission_update"
    PRICE_UPDATE = "price_update"
    BROCHURE = "brochure"
    NEWS = "news"
    GENERAL_INFORMATION = "general_information"
