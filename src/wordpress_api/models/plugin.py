"""Plugin models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class Plugin(WordPressModel):
    """WordPress Plugin object."""

    plugin: str = ""
    status: str = "inactive"
    name: str = ""
    plugin_uri: str = ""
    author: str = ""
    author_uri: str = ""
    description: dict[str, str] = Field(default_factory=dict)
    version: str = ""
    network_only: bool = False
    requires_wp: str = ""
    requires_php: str = ""
    textdomain: str = ""


class PluginActivate(WordPressModel):
    """Data for activating a plugin."""

    status: str = "active"


class PluginDeactivate(WordPressModel):
    """Data for deactivating a plugin."""

    status: str = "inactive"
