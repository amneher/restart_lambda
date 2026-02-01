"""Post Statuses endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .base import BaseEndpoint


class PostStatusInfo(BaseModel):
    """WordPress Post Status object."""

    name: str = ""
    slug: str = ""
    public: bool = True
    queryable: bool = True
    date_floating: bool = False


class StatusesEndpoint(BaseEndpoint):
    """Endpoint for viewing WordPress post statuses."""

    _path = "/wp/v2/statuses"

    def list(self, **kwargs: Any) -> dict[str, PostStatusInfo]:
        """List all registered post statuses."""
        response = self._get(self._path, params=kwargs)
        return {k: PostStatusInfo.model_validate(v) for k, v in response.items()}

    def get(self, status: str, **kwargs: Any) -> PostStatusInfo:
        """Get a specific post status by slug."""
        response = self._get(f"{self._path}/{status}", params=kwargs)
        return PostStatusInfo.model_validate(response)

    def get_publish(self) -> PostStatusInfo:
        """Get the 'publish' status."""
        return self.get("publish")

    def get_draft(self) -> PostStatusInfo:
        """Get the 'draft' status."""
        return self.get("draft")

    def get_pending(self) -> PostStatusInfo:
        """Get the 'pending' status."""
        return self.get("pending")

    def get_private(self) -> PostStatusInfo:
        """Get the 'private' status."""
        return self.get("private")

    def list_public(self) -> dict[str, PostStatusInfo]:
        """List only public post statuses."""
        all_statuses = self.list()
        return {k: v for k, v in all_statuses.items() if v.public}
