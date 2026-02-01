"""Posts endpoint."""

from __future__ import annotations

from typing import Any

from ..models.post import Post, PostCreate, PostUpdate, PostStatus
from .base import CRUDEndpoint


class PostsEndpoint(CRUDEndpoint[Post]):
    """Endpoint for managing WordPress posts."""

    _path = "/wp/v2/posts"
    _model_class = Post

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "desc",
        orderby: str = "date",
        status: str | PostStatus | list[str] | None = None,
        categories: list[int] | None = None,
        categories_exclude: list[int] | None = None,
        tags: list[int] | None = None,
        tags_exclude: list[int] | None = None,
        author: int | list[int] | None = None,
        author_exclude: list[int] | None = None,
        before: str | None = None,
        after: str | None = None,
        modified_before: str | None = None,
        modified_after: str | None = None,
        slug: str | list[str] | None = None,
        sticky: bool | None = None,
        **kwargs: Any,
    ) -> list[Post]:
        """List posts with filtering options.
        
        Args:
            page: Current page of the collection.
            per_page: Maximum number of items to return.
            search: Limit results to those matching a string.
            order: Order sort attribute ascending or descending.
            orderby: Sort collection by attribute.
            status: Limit result set to posts with specific status(es).
            categories: Limit result set to posts with specific categories.
            categories_exclude: Exclude posts with specific categories.
            tags: Limit result set to posts with specific tags.
            tags_exclude: Exclude posts with specific tags.
            author: Limit result set to posts by specific author(s).
            author_exclude: Exclude posts by specific authors.
            before: Limit to posts published before a given date.
            after: Limit to posts published after a given date.
            modified_before: Limit to posts modified before a given date.
            modified_after: Limit to posts modified after a given date.
            slug: Limit result set to posts with specific slug(s).
            sticky: Limit result set to sticky or non-sticky posts.
        """
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        
        if search:
            params["search"] = search
        if status:
            if isinstance(status, PostStatus):
                params["status"] = status.value
            elif isinstance(status, list):
                params["status"] = ",".join(status)
            else:
                params["status"] = status
        if categories:
            params["categories"] = ",".join(map(str, categories))
        if categories_exclude:
            params["categories_exclude"] = ",".join(map(str, categories_exclude))
        if tags:
            params["tags"] = ",".join(map(str, tags))
        if tags_exclude:
            params["tags_exclude"] = ",".join(map(str, tags_exclude))
        if author is not None:
            if isinstance(author, list):
                params["author"] = ",".join(map(str, author))
            else:
                params["author"] = author
        if author_exclude:
            params["author_exclude"] = ",".join(map(str, author_exclude))
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if modified_before:
            params["modified_before"] = modified_before
        if modified_after:
            params["modified_after"] = modified_after
        if slug:
            if isinstance(slug, list):
                params["slug"] = ",".join(slug)
            else:
                params["slug"] = slug
        if sticky is not None:
            params["sticky"] = sticky

        params.update(kwargs)
        response = self._get(self._path, params=params)
        return [Post.model_validate(item) for item in response]

    def create(self, data: PostCreate | dict[str, Any]) -> Post:
        """Create a new post."""
        return super().create(data)

    def update(self, id: int, data: PostUpdate | dict[str, Any]) -> Post:
        """Update an existing post."""
        return super().update(id, data)

    def trash(self, id: int) -> Post:
        """Move a post to trash."""
        return self.update(id, PostUpdate(status=PostStatus.TRASH))

    def restore(self, id: int) -> Post:
        """Restore a post from trash."""
        return self.update(id, PostUpdate(status=PostStatus.DRAFT))

    def get_by_slug(self, slug: str) -> Post | None:
        """Get a post by its slug."""
        posts = self.list(slug=slug)
        return posts[0] if posts else None
