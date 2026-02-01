"""Page models."""

from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from .base import WordPressModel, RenderedContent, parse_datetime
from .post import PostStatus


class Page(WordPressModel):
    """WordPress Page object."""

    id: int
    date: datetime | None = None
    date_gmt: datetime | None = None
    guid: RenderedContent | None = None
    modified: datetime | None = None
    modified_gmt: datetime | None = None
    slug: str = ""
    status: PostStatus = PostStatus.DRAFT
    type: str = "page"
    link: str = ""
    title: RenderedContent | None = None
    content: RenderedContent | None = None
    excerpt: RenderedContent | None = None
    author: int = 0
    featured_media: int = 0
    parent: int = 0
    menu_order: int = 0
    comment_status: str = "closed"
    ping_status: str = "closed"
    template: str = ""
    meta: dict[str, Any] = Field(default_factory=dict)

    @field_validator("date", "date_gmt", "modified", "modified_gmt", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class PageCreate(WordPressModel):
    """Data for creating a new page."""

    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    status: PostStatus = PostStatus.DRAFT
    author: int | None = None
    featured_media: int | None = None
    parent: int | None = None
    menu_order: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    template: str | None = None
    meta: dict[str, Any] | None = None
    slug: str | None = None
    date: datetime | str | None = None
    password: str | None = None


class PageUpdate(WordPressModel):
    """Data for updating a page."""

    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    status: PostStatus | None = None
    author: int | None = None
    featured_media: int | None = None
    parent: int | None = None
    menu_order: int | None = None
    comment_status: str | None = None
    ping_status: str | None = None
    template: str | None = None
    meta: dict[str, Any] | None = None
    slug: str | None = None
    date: datetime | str | None = None
    password: str | None = None
