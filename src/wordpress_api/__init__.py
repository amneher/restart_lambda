"""
WordPress REST API Python Client

A full-featured Python 3.12 interface to the WordPress REST API.
"""

from .client import WordPressClient
from .auth import ApplicationPasswordAuth, BasicAuth, JWTAuth, OAuth2Auth
from .exceptions import (
    WordPressError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)

__version__ = "1.0.0"
__all__ = [
    "WordPressClient",
    "ApplicationPasswordAuth",
    "BasicAuth",
    "JWTAuth",
    "OAuth2Auth",
    "WordPressError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
]
