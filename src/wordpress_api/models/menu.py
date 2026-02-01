"""Menu models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class MenuItem(WordPressModel):
    """WordPress Menu Item object."""

    id: int
    title: str = ""
    status: str = "publish"
    url: str = ""
    attr_title: str = ""
    description: str = ""
    type: str = "custom"
    type_label: str = ""
    object: str = "custom"
    object_id: int = 0
    parent: int = 0
    menu_order: int = 0
    target: str = ""
    classes: list[str] = Field(default_factory=list)
    xfn: list[str] = Field(default_factory=list)
    invalid: bool = False
    menus: int = 0
    meta: dict[str, Any] = Field(default_factory=dict)


class Menu(WordPressModel):
    """WordPress Navigation Menu object."""

    id: int
    name: str = ""
    slug: str = ""
    description: str = ""
    count: int = 0
    auto_add: bool = False
    locations: list[str] = Field(default_factory=list)
    meta: dict[str, Any] = Field(default_factory=dict)


class MenuItemCreate(WordPressModel):
    """Data for creating a menu item."""

    title: str
    url: str | None = None
    status: str = "publish"
    attr_title: str | None = None
    description: str | None = None
    type: str = "custom"
    object: str | None = None
    object_id: int | None = None
    parent: int | None = None
    menu_order: int | None = None
    target: str | None = None
    classes: list[str] | None = None
    xfn: list[str] | None = None
    menus: int | None = None
    meta: dict[str, Any] | None = None


class MenuItemUpdate(WordPressModel):
    """Data for updating a menu item."""

    title: str | None = None
    url: str | None = None
    status: str | None = None
    attr_title: str | None = None
    description: str | None = None
    type: str | None = None
    object: str | None = None
    object_id: int | None = None
    parent: int | None = None
    menu_order: int | None = None
    target: str | None = None
    classes: list[str] | None = None
    xfn: list[str] | None = None
    menus: int | None = None
    meta: dict[str, Any] | None = None
