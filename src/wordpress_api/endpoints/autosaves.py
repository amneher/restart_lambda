"""Autosaves endpoint."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from ..models.base import RenderedContent, parse_datetime
from .base import BaseEndpoint


class Autosave(BaseModel):
    """WordPress Autosave object."""

    id: int
    author: int = 0
    date: datetime | None = None
    date_gmt: datetime | None = None
    modified: datetime | None = None
    modified_gmt: datetime | None = None
    parent: int = 0
    slug: str = ""
    title: RenderedContent | None = None
    content: RenderedContent | None = None
    excerpt: RenderedContent | None = None

    @field_validator("date", "date_gmt", "modified", "modified_gmt", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class AutosavesEndpoint(BaseEndpoint):
    """Endpoint for managing post and page autosaves."""

    def list_post_autosaves(self, post_id: int, **kwargs: Any) -> list[Autosave]:
        """List autosaves for a post."""
        response = self._get(f"/wp/v2/posts/{post_id}/autosaves", params=kwargs)
        return [Autosave.model_validate(item) for item in response]

    def get_post_autosave(self, post_id: int, autosave_id: int) -> Autosave:
        """Get a specific post autosave."""
        response = self._get(f"/wp/v2/posts/{post_id}/autosaves/{autosave_id}")
        return Autosave.model_validate(response)

    def create_post_autosave(
        self,
        post_id: int,
        title: str | None = None,
        content: str | None = None,
        excerpt: str | None = None,
        **kwargs: Any,
    ) -> Autosave:
        """Create an autosave for a post."""
        data: dict[str, Any] = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if excerpt:
            data["excerpt"] = excerpt
        data.update(kwargs)
        
        response = self._post(f"/wp/v2/posts/{post_id}/autosaves", data=data)
        return Autosave.model_validate(response)

    def list_page_autosaves(self, page_id: int, **kwargs: Any) -> list[Autosave]:
        """List autosaves for a page."""
        response = self._get(f"/wp/v2/pages/{page_id}/autosaves", params=kwargs)
        return [Autosave.model_validate(item) for item in response]

    def get_page_autosave(self, page_id: int, autosave_id: int) -> Autosave:
        """Get a specific page autosave."""
        response = self._get(f"/wp/v2/pages/{page_id}/autosaves/{autosave_id}")
        return Autosave.model_validate(response)

    def create_page_autosave(
        self,
        page_id: int,
        title: str | None = None,
        content: str | None = None,
        excerpt: str | None = None,
        **kwargs: Any,
    ) -> Autosave:
        """Create an autosave for a page."""
        data: dict[str, Any] = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if excerpt:
            data["excerpt"] = excerpt
        data.update(kwargs)
        
        response = self._post(f"/wp/v2/pages/{page_id}/autosaves", data=data)
        return Autosave.model_validate(response)

    def get_latest_autosave(self, post_id: int, post_type: str = "posts") -> Autosave | None:
        """Get the most recent autosave."""
        if post_type == "pages":
            autosaves = self.list_page_autosaves(post_id)
        else:
            autosaves = self.list_post_autosaves(post_id)
        return autosaves[0] if autosaves else None
