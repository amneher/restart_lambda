"""Comment models."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field, field_validator

from .base import WordPressModel, RenderedContent, parse_datetime


class CommentStatus(str, Enum):
    """Comment status options."""

    APPROVED = "approved"
    HOLD = "hold"
    SPAM = "spam"
    TRASH = "trash"


class Comment(WordPressModel):
    """WordPress Comment object."""

    id: int
    post: int = 0
    parent: int = 0
    author: int = 0
    author_name: str = ""
    author_email: str = ""
    author_url: str = ""
    author_ip: str = ""
    author_user_agent: str = ""
    date: datetime | None = None
    date_gmt: datetime | None = None
    content: RenderedContent | None = None
    link: str = ""
    status: str = "approved"
    type: str = "comment"
    author_avatar_urls: dict[str, str] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)

    @field_validator("date", "date_gmt", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class CommentCreate(WordPressModel):
    """Data for creating a new comment."""

    post: int
    content: str
    parent: int | None = None
    author: int | None = None
    author_name: str | None = None
    author_email: str | None = None
    author_url: str | None = None
    status: CommentStatus | None = None
    meta: dict[str, Any] | None = None
    date: datetime | str | None = None


class CommentUpdate(WordPressModel):
    """Data for updating a comment."""

    content: str | None = None
    post: int | None = None
    parent: int | None = None
    author: int | None = None
    author_name: str | None = None
    author_email: str | None = None
    author_url: str | None = None
    status: CommentStatus | None = None
    meta: dict[str, Any] | None = None
    date: datetime | str | None = None
