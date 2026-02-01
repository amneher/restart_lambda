"""Category models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class Category(WordPressModel):
    """WordPress Category object."""

    id: int
    count: int = 0
    description: str = ""
    link: str = ""
    name: str = ""
    slug: str = ""
    taxonomy: str = "category"
    parent: int = 0
    meta: dict[str, Any] = Field(default_factory=dict)


class CategoryCreate(WordPressModel):
    """Data for creating a new category."""

    name: str
    description: str | None = None
    slug: str | None = None
    parent: int | None = None
    meta: dict[str, Any] | None = None


class CategoryUpdate(WordPressModel):
    """Data for updating a category."""

    name: str | None = None
    description: str | None = None
    slug: str | None = None
    parent: int | None = None
    meta: dict[str, Any] | None = None
