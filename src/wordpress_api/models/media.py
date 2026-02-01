"""Media models."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field, field_validator

from .base import WordPressModel, RenderedContent, parse_datetime


class MediaType(str, Enum):
    """Media type options."""

    IMAGE = "image"
    FILE = "file"
    AUDIO = "audio"
    VIDEO = "video"
    APPLICATION = "application"


class MediaSize(WordPressModel):
    """Individual media size details."""

    file: str = ""
    width: int = 0
    height: int = 0
    mime_type: str = ""
    source_url: str = ""


class MediaDetails(WordPressModel):
    """Media file details."""

    width: int = 0
    height: int = 0
    file: str = ""
    filesize: int = 0
    sizes: dict[str, MediaSize] = Field(default_factory=dict)
    image_meta: dict[str, Any] = Field(default_factory=dict)


class Media(WordPressModel):
    """WordPress Media object."""

    id: int
    date: datetime | None = None
    date_gmt: datetime | None = None
    guid: RenderedContent | None = None
    modified: datetime | None = None
    modified_gmt: datetime | None = None
    slug: str = ""
    status: str = "inherit"
    type: str = "attachment"
    link: str = ""
    title: RenderedContent | None = None
    author: int = 0
    comment_status: str = "open"
    ping_status: str = "closed"
    template: str = ""
    meta: dict[str, Any] = Field(default_factory=dict)
    description: RenderedContent | None = None
    caption: RenderedContent | None = None
    alt_text: str = ""
    media_type: str = ""
    mime_type: str = ""
    media_details: MediaDetails | None = None
    post: int | None = None
    source_url: str = ""

    @field_validator("date", "date_gmt", "modified", "modified_gmt", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class MediaCreate(WordPressModel):
    """Data for creating/uploading new media."""

    title: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    description: str | None = None
    post: int | None = None
    author: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    meta: dict[str, Any] | None = None
    slug: str | None = None
    status: str | None = None
    date: datetime | str | None = None


class MediaUpdate(WordPressModel):
    """Data for updating media."""

    title: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    description: str | None = None
    post: int | None = None
    author: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    meta: dict[str, Any] | None = None
    slug: str | None = None
    status: str | None = None
    date: datetime | str | None = None
