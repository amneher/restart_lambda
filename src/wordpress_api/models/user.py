"""User models."""

from enum import Enum
from typing import Any

from pydantic import Field

from .base import WordPressModel


class UserRole(str, Enum):
    """Default WordPress user roles."""

    ADMINISTRATOR = "administrator"
    EDITOR = "editor"
    AUTHOR = "author"
    CONTRIBUTOR = "contributor"
    SUBSCRIBER = "subscriber"


class UserCapabilities(WordPressModel):
    """User capabilities."""

    pass


class User(WordPressModel):
    """WordPress User object."""

    id: int
    username: str = ""
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    url: str = ""
    description: str = ""
    link: str = ""
    locale: str = ""
    nickname: str = ""
    slug: str = ""
    registered_date: str = ""
    roles: list[str] = Field(default_factory=list)
    capabilities: dict[str, bool] = Field(default_factory=dict)
    extra_capabilities: dict[str, bool] = Field(default_factory=dict)
    avatar_urls: dict[str, str] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)


class UserCreate(WordPressModel):
    """Data for creating a new user."""

    username: str
    email: str
    password: str
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    url: str | None = None
    description: str | None = None
    locale: str | None = None
    nickname: str | None = None
    slug: str | None = None
    roles: list[str] | None = None
    meta: dict[str, Any] | None = None


class UserUpdate(WordPressModel):
    """Data for updating a user."""

    email: str | None = None
    password: str | None = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    url: str | None = None
    description: str | None = None
    locale: str | None = None
    nickname: str | None = None
    slug: str | None = None
    roles: list[str] | None = None
    meta: dict[str, Any] | None = None
