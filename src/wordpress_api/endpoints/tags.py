"""Tags endpoint."""

from typing import Any

from ..models.tag import Tag, TagCreate, TagUpdate
from .base import CRUDEndpoint


class TagsEndpoint(CRUDEndpoint[Tag]):
    """Endpoint for managing WordPress tags."""

    _path = "/wp/v2/tags"
    _model_class = Tag

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "asc",
        orderby: str = "name",
        hide_empty: bool = False,
        post: int | None = None,
        slug: str | list[str] | None = None,
        include: list[int] | None = None,
        exclude: list[int] | None = None,
        **kwargs: Any,
    ) -> list[Tag]:
        """List tags with filtering options."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
            "hide_empty": hide_empty,
        }
        
        if search:
            params["search"] = search
        if post is not None:
            params["post"] = post
        if slug:
            if isinstance(slug, list):
                params["slug"] = ",".join(slug)
            else:
                params["slug"] = slug
        if include:
            params["include"] = ",".join(map(str, include))
        if exclude:
            params["exclude"] = ",".join(map(str, exclude))

        params.update(kwargs)
        response = self._get(self._path, params=params)
        return [Tag.model_validate(item) for item in response]

    def create(self, data: TagCreate | dict[str, Any]) -> Tag:
        """Create a new tag."""
        return super().create(data)

    def update(self, id: int, data: TagUpdate | dict[str, Any]) -> Tag:
        """Update an existing tag."""
        return super().update(id, data)

    def get_by_slug(self, slug: str) -> Tag | None:
        """Get a tag by its slug."""
        tags = self.list(slug=slug)
        return tags[0] if tags else None

    def get_for_post(self, post_id: int) -> list[Tag]:
        """Get tags assigned to a specific post."""
        return self.list(post=post_id)

    def get_popular(self, limit: int = 10) -> list[Tag]:
        """Get the most popular tags by post count."""
        all_tags = list(self.iterate_all(hide_empty=True))
        sorted_tags = sorted(all_tags, key=lambda t: t.count, reverse=True)
        return sorted_tags[:limit]
