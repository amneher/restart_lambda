"""Theme models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class ThemeSupports(WordPressModel):
    """Theme feature support."""

    align_wide: bool = False
    automatic_feed_links: bool = True
    custom_background: bool | dict = False
    custom_header: bool | dict = False
    custom_logo: bool | dict = False
    customize_selective_refresh_widgets: bool = False
    dark_editor_style: bool = False
    editor_color_palette: bool | list = False
    editor_font_sizes: bool | list = False
    editor_gradient_presets: bool | list = False
    editor_styles: bool = False
    html5: bool | list = False
    formats: list[str] = Field(default_factory=list)
    post_thumbnails: bool | list = True
    responsive_embeds: bool = False
    title_tag: bool = False
    wp_block_styles: bool = False


class Theme(WordPressModel):
    """WordPress Theme object."""

    stylesheet: str = ""
    template: str = ""
    author: dict[str, str] = Field(default_factory=dict)
    author_uri: dict[str, str] = Field(default_factory=dict)
    description: dict[str, str] = Field(default_factory=dict)
    name: dict[str, str] = Field(default_factory=dict)
    requires_php: str = ""
    requires_wp: str = ""
    screenshot: str = ""
    tags: dict[str, list[str]] = Field(default_factory=dict)
    textdomain: str = ""
    theme_supports: ThemeSupports | None = None
    theme_uri: dict[str, str] = Field(default_factory=dict)
    version: str = ""
    status: str = "inactive"
    is_block_theme: bool = False
