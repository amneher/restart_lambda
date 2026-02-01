"""Search endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .base import BaseEndpoint


class SearchResult(BaseModel):
    """WordPress search result."""

    id: int
    title: str = ""
    url: str = ""
    type: str = ""
    subtype: str = ""


class SearchEndpoint(BaseEndpoint):
    """Endpoint for WordPress site-wide search."""

    _path = "/wp/v2/search"

    def search(
        self,
        search: str,
        page: int = 1,
        per_page: int = 10,
        type: str | None = None,
        subtype: str | list[str] | None = None,
        **kwargs: Any,
    ) -> list[SearchResult]:
        """Search the site.
        
        Args:
            search: Search query string.
            page: Current page of the collection.
            per_page: Maximum number of items to return.
            type: Limit results to a specific type (post, term, post-format).
            subtype: Limit results to specific subtypes (post, page, category, etc.).
        """
        params: dict[str, Any] = {
            "search": search,
            "page": page,
            "per_page": per_page,
        }
        
        if type:
            params["type"] = type
        if subtype:
            if isinstance(subtype, list):
                params["subtype"] = ",".join(subtype)
            else:
                params["subtype"] = subtype
        params.update(kwargs)
        
        response = self._get(self._path, params=params)
        return [SearchResult.model_validate(item) for item in response]

    def search_posts(self, query: str, **kwargs: Any) -> list[SearchResult]:
        """Search only posts."""
        return self.search(query, type="post", subtype="post", **kwargs)

    def search_pages(self, query: str, **kwargs: Any) -> list[SearchResult]:
        """Search only pages."""
        return self.search(query, type="post", subtype="page", **kwargs)

    def search_categories(self, query: str, **kwargs: Any) -> list[SearchResult]:
        """Search only categories."""
        return self.search(query, type="term", subtype="category", **kwargs)

    def search_tags(self, query: str, **kwargs: Any) -> list[SearchResult]:
        """Search only tags."""
        return self.search(query, type="term", subtype="post_tag", **kwargs)

    def search_all_content(self, query: str, **kwargs: Any) -> list[SearchResult]:
        """Search all post types (posts, pages, custom post types)."""
        return self.search(query, type="post", **kwargs)
