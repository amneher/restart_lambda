"""Revisions endpoint."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..models.base import RenderedContent, parse_datetime
from .base import BaseEndpoint


class Revision(BaseModel):
    """WordPress Revision object."""

    id: int
    author: int = 0
    date: datetime | None = None
    date_gmt: datetime | None = None
    guid: RenderedContent | None = None
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


class RevisionsEndpoint(BaseEndpoint):
    """Endpoint for managing post and page revisions."""

    def list_post_revisions(
        self,
        post_id: int,
        page: int = 1,
        per_page: int = 10,
        **kwargs: Any,
    ) -> list[Revision]:
        """List revisions for a post."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        params.update(kwargs)
        
        response = self._get(f"/wp/v2/posts/{post_id}/revisions", params=params)
        return [Revision.model_validate(item) for item in response]

    def get_post_revision(self, post_id: int, revision_id: int) -> Revision:
        """Get a specific post revision."""
        response = self._get(f"/wp/v2/posts/{post_id}/revisions/{revision_id}")
        return Revision.model_validate(response)

    def delete_post_revision(
        self,
        post_id: int,
        revision_id: int,
        force: bool = True,
    ) -> dict[str, Any]:
        """Delete a post revision."""
        return self._delete(
            f"/wp/v2/posts/{post_id}/revisions/{revision_id}",
            params={"force": force},
        )

    def list_page_revisions(
        self,
        page_id: int,
        page: int = 1,
        per_page: int = 10,
        **kwargs: Any,
    ) -> list[Revision]:
        """List revisions for a page."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        params.update(kwargs)
        
        response = self._get(f"/wp/v2/pages/{page_id}/revisions", params=params)
        return [Revision.model_validate(item) for item in response]

    def get_page_revision(self, page_id: int, revision_id: int) -> Revision:
        """Get a specific page revision."""
        response = self._get(f"/wp/v2/pages/{page_id}/revisions/{revision_id}")
        return Revision.model_validate(response)

    def delete_page_revision(
        self,
        page_id: int,
        revision_id: int,
        force: bool = True,
    ) -> dict[str, Any]:
        """Delete a page revision."""
        return self._delete(
            f"/wp/v2/pages/{page_id}/revisions/{revision_id}",
            params={"force": force},
        )

    def get_latest_revision(self, post_id: int, post_type: str = "posts") -> Revision | None:
        """Get the most recent revision."""
        if post_type == "pages":
            revisions = self.list_page_revisions(post_id, per_page=1)
        else:
            revisions = self.list_post_revisions(post_id, per_page=1)
        return revisions[0] if revisions else None

    def count_revisions(self, post_id: int, post_type: str = "posts") -> int:
        """Count the number of revisions for a post or page."""
        if post_type == "pages":
            all_revisions = self.list_page_revisions(post_id, per_page=100)
        else:
            all_revisions = self.list_post_revisions(post_id, per_page=100)
        return len(all_revisions)
