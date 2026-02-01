"""Post models."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field, field_validator

from .base import WordPressModel, RenderedContent, parse_datetime


class PostStatus(str, Enum):
    """Post status options."""

    PUBLISH = "publish"
    FUTURE = "future"
    DRAFT = "draft"
    PENDING = "pending"
    PRIVATE = "private"
    TRASH = "trash"


class PostFormat(str, Enum):
    """Post format options."""

    STANDARD = "standard"
    ASIDE = "aside"
    CHAT = "chat"
    GALLERY = "gallery"
    LINK = "link"
    IMAGE = "image"
    QUOTE = "quote"
    STATUS = "status"
    VIDEO = "video"
    AUDIO = "audio"


class Post(WordPressModel):
    """WordPress Post object."""

    id: int
    date: datetime | None = None
    date_gmt: datetime | None = None
    guid: RenderedContent | None = None
    modified: datetime | None = None
    modified_gmt: datetime | None = None
    slug: str = ""
    status: PostStatus = PostStatus.DRAFT
    type: str = "post"
    link: str = ""
    title: RenderedContent | None = None
    content: RenderedContent | None = None
    excerpt: RenderedContent | None = None
    author: int = 0
    featured_media: int = 0
    comment_status: str = "open"
    ping_status: str = "open"
    sticky: bool = False
    template: str = ""
    format: PostFormat = PostFormat.STANDARD
    meta: dict[str, Any] = Field(default_factory=dict)
    categories: list[int] = Field(default_factory=list)
    tags: list[int] = Field(default_factory=list)

    @field_validator("date", "date_gmt", "modified", "modified_gmt", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class PostCreate(WordPressModel):
    """Data for creating a new post."""

    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    status: PostStatus = PostStatus.DRAFT
    author: int | None = None
    featured_media: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    format: PostFormat | None = None
    sticky: bool | None = None
    categories: list[int] | None = None
    tags: list[int] | None = None
    meta: dict[str, Any] | None = None
    template: str | None = None
    slug: str | None = None
    date: datetime | str | None = None
    password: str | None = None


class PostUpdate(WordPressModel):
    """Data for updating a post."""

    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    status: PostStatus | None = None
    author: int | None = None
    featured_media: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    format: PostFormat | None = None
    sticky: bool | None = None
    categories: list[int] | None = None
    tags: list[int] | None = None
    meta: dict[str, Any] | None = None
    template: str | None = None
    slug: str | None = None
    date: datetime | str | None = None
    password: str | None = None
