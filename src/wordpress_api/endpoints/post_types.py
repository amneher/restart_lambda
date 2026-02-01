"""Post Types endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .base import BaseEndpoint


class PostType(BaseModel):
    """WordPress Post Type object."""

    name: str = ""
    slug: str = ""
    description: str = ""
    hierarchical: bool = False
    has_archive: bool = False
    rest_base: str = ""
    rest_namespace: str = "wp/v2"
    taxonomies: list[str] = Field(default_factory=list)
    capabilities: dict[str, str] = Field(default_factory=dict)
    labels: dict[str, str] = Field(default_factory=dict)
    supports: dict[str, bool] = Field(default_factory=dict)
    icon: str | None = None
    viewable: bool = True
    visibility: dict[str, bool] = Field(default_factory=dict)


class PostTypesEndpoint(BaseEndpoint):
    """Endpoint for viewing WordPress post types."""

    _path = "/wp/v2/types"

    def list(self, **kwargs: Any) -> dict[str, PostType]:
        """List all registered post types."""
        response = self._get(self._path, params=kwargs)
        return {k: PostType.model_validate(v) for k, v in response.items()}

    def get(self, post_type: str, **kwargs: Any) -> PostType:
        """Get a specific post type by slug."""
        response = self._get(f"{self._path}/{post_type}", params=kwargs)
        return PostType.model_validate(response)

    def get_post(self) -> PostType:
        """Get the 'post' post type."""
        return self.get("post")

    def get_page(self) -> PostType:
        """Get the 'page' post type."""
        return self.get("page")

    def get_attachment(self) -> PostType:
        """Get the 'attachment' post type."""
        return self.get("attachment")

    def list_public(self) -> dict[str, PostType]:
        """List only publicly viewable post types."""
        all_types = self.list()
        return {k: v for k, v in all_types.items() if v.viewable}
