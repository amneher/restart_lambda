"""WordPress API Exception Classes."""

from typing import Any


class WordPressError(Exception):
    """Base exception for WordPress API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_code: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.data = data or {}

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"[HTTP {self.status_code}]")
        if self.error_code:
            parts.append(f"[{self.error_code}]")
        return " ".join(parts)


class AuthenticationError(WordPressError):
    """Authentication failed."""
    pass


class NotFoundError(WordPressError):
    """Resource not found."""
    pass


class ValidationError(WordPressError):
    """Validation error in request data."""
    pass


class RateLimitError(WordPressError):
    """Rate limit exceeded."""
    pass


class ServerError(WordPressError):
    """Server-side error."""
    pass


class PermissionError(WordPressError):
    """Permission denied."""
    pass


def raise_for_status(status_code: int, response_data: dict[str, Any]) -> None:
    """Raise appropriate exception based on status code."""
    message = response_data.get("message", "Unknown error")
    error_code = response_data.get("code", "unknown_error")

    if status_code == 401:
        raise AuthenticationError(message, status_code, error_code, response_data)
    elif status_code == 403:
        raise PermissionError(message, status_code, error_code, response_data)
    elif status_code == 404:
        raise NotFoundError(message, status_code, error_code, response_data)
    elif status_code == 400:
        raise ValidationError(message, status_code, error_code, response_data)
    elif status_code == 429:
        raise RateLimitError(message, status_code, error_code, response_data)
    elif status_code >= 500:
        raise ServerError(message, status_code, error_code, response_data)
    elif status_code >= 400:
        raise WordPressError(message, status_code, error_code, response_data)
