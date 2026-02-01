"""Tag models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class Tag(WordPressModel):
    """WordPress Tag object."""

    id: int
    count: int = 0
    description: str = ""
    link: str = ""
    name: str = ""
    slug: str = ""
    taxonomy: str = "post_tag"
    meta: dict[str, Any] = Field(default_factory=dict)


class TagCreate(WordPressModel):
    """Data for creating a new tag."""

    name: str
    description: str | None = None
    slug: str | None = None
    meta: dict[str, Any] | None = None


class TagUpdate(WordPressModel):
    """Data for updating a tag."""

    name: str | None = None
    description: str | None = None
    slug: str | None = None
    meta: dict[str, Any] | None = None
