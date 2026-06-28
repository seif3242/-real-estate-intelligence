"""Exceptions raised by WhatsApp provider implementations."""


class ProviderError(Exception):
    """Base class for all provider-related errors."""


class SessionExpiredError(ProviderError):
    """Raised when the provider's session is fully invalidated and requires manual
    re-authentication (e.g. a fresh QR scan). Must surface as a Dashboard notification
    once the Notification Service exists (System Design §2.3) — never fail silently."""


class ConnectionLostError(ProviderError):
    """Raised when the provider unexpectedly loses connectivity but the session itself
    may still be valid; callers should retry with backoff before raising SessionExpiredError."""
