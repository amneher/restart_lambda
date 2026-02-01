"""Base models and utilities."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class WordPressModel(BaseModel):
    """Base model for WordPress objects."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class RenderedContent(BaseModel):
    """Content with rendered HTML."""

    rendered: str = ""
    raw: str | None = None
    protected: bool = False

    model_config = ConfigDict(extra="allow")


class WPLink(BaseModel):
    """WordPress REST API link."""

    href: str
    embeddable: bool = False

    model_config = ConfigDict(extra="allow")


class WPLinks(BaseModel):
    """Collection of WordPress REST API links."""

    self_: list[WPLink] | None = None
    collection: list[WPLink] | None = None
    about: list[WPLink] | None = None
    author: list[WPLink] | None = None
    replies: list[WPLink] | None = None
    version_history: list[WPLink] | None = None
    predecessor_version: list[WPLink] | None = None
    wp_attachment: list[WPLink] | None = None
    wp_term: list[WPLink] | None = None
    curies: list[WPLink] | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


def parse_datetime(value: Any) -> datetime | None:
    """Parse WordPress datetime string."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None
