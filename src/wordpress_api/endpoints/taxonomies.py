"""Taxonomies endpoint."""

from __future__ import annotations

from typing import Any

from ..models.taxonomy import Taxonomy
from .base import BaseEndpoint


class TaxonomiesEndpoint(BaseEndpoint):
    """Endpoint for viewing WordPress taxonomies."""

    _path = "/wp/v2/taxonomies"

    def list(self, type: str | None = None, **kwargs: Any) -> dict[str, Taxonomy]:
        """List all taxonomies.
        
        Args:
            type: Limit results to taxonomies associated with a post type.
        """
        params: dict[str, Any] = {}
        if type:
            params["type"] = type
        params.update(kwargs)
        
        response = self._get(self._path, params=params)
        return {k: Taxonomy.model_validate(v) for k, v in response.items()}

    def get(self, taxonomy: str, **kwargs: Any) -> Taxonomy:
        """Get a specific taxonomy by slug."""
        response = self._get(f"{self._path}/{taxonomy}", params=kwargs)
        return Taxonomy.model_validate(response)

    def get_category(self) -> Taxonomy:
        """Get the category taxonomy."""
        return self.get("category")

    def get_post_tag(self) -> Taxonomy:
        """Get the post_tag taxonomy."""
        return self.get("post_tag")
