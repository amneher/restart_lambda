"""Settings models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class Settings(WordPressModel):
    """WordPress Site Settings."""

    title: str = ""
    description: str = ""
    url: str = ""
    email: str = ""
    timezone: str = ""
    date_format: str = ""
    time_format: str = ""
    start_of_week: int = 0
    language: str = ""
    use_smilies: bool = True
    default_category: int = 1
    default_post_format: str = ""
    posts_per_page: int = 10
    default_ping_status: str = "open"
    default_comment_status: str = "open"
    show_on_front: str = "posts"
    page_on_front: int = 0
    page_for_posts: int = 0
    site_logo: int | None = None
    site_icon: int | None = None
