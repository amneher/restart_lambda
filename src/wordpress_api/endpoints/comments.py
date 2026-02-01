"""Comments endpoint."""

from __future__ import annotations

from typing import Any

from ..models.comment import Comment, CommentCreate, CommentUpdate, CommentStatus
from .base import CRUDEndpoint


class CommentsEndpoint(CRUDEndpoint[Comment]):
    """Endpoint for managing WordPress comments."""

    _path = "/wp/v2/comments"
    _model_class = Comment

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "desc",
        orderby: str = "date_gmt",
        status: str | CommentStatus | None = None,
        post: int | list[int] | None = None,
        parent: int | list[int] | None = None,
        parent_exclude: list[int] | None = None,
        author: int | list[int] | None = None,
        author_exclude: list[int] | None = None,
        author_email: str | None = None,
        before: str | None = None,
        after: str | None = None,
        type: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> list[Comment]:
        """List comments with filtering options."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        
        if search:
            params["search"] = search
        if status:
            if isinstance(status, CommentStatus):
                params["status"] = status.value
            else:
                params["status"] = status
        if post is not None:
            if isinstance(post, list):
                params["post"] = ",".join(map(str, post))
            else:
                params["post"] = post
        if parent is not None:
            if isinstance(parent, list):
                params["parent"] = ",".join(map(str, parent))
            else:
                params["parent"] = parent
        if parent_exclude:
            params["parent_exclude"] = ",".join(map(str, parent_exclude))
        if author is not None:
            if isinstance(author, list):
                params["author"] = ",".join(map(str, author))
            else:
                params["author"] = author
        if author_exclude:
            params["author_exclude"] = ",".join(map(str, author_exclude))
        if author_email:
            params["author_email"] = author_email
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if type:
            params["type"] = type
        if password:
            params["password"] = password

        params.update(kwargs)
        response = self._get(self._path, params=params)
        return [Comment.model_validate(item) for item in response]

    def create(self, data: CommentCreate | dict[str, Any]) -> Comment:
        """Create a new comment."""
        return super().create(data)

    def update(self, id: int, data: CommentUpdate | dict[str, Any]) -> Comment:
        """Update an existing comment."""
        return super().update(id, data)

    def approve(self, id: int) -> Comment:
        """Approve a comment."""
        return self.update(id, CommentUpdate(status=CommentStatus.APPROVED))

    def unapprove(self, id: int) -> Comment:
        """Put a comment on hold."""
        return self.update(id, CommentUpdate(status=CommentStatus.HOLD))

    def spam(self, id: int) -> Comment:
        """Mark a comment as spam."""
        return self.update(id, CommentUpdate(status=CommentStatus.SPAM))

    def trash(self, id: int) -> Comment:
        """Move a comment to trash."""
        return self.update(id, CommentUpdate(status=CommentStatus.TRASH))

    def list_for_post(self, post_id: int, **kwargs: Any) -> list[Comment]:
        """List all comments for a specific post."""
        return self.list(post=post_id, **kwargs)

    def list_replies(self, parent_id: int, **kwargs: Any) -> list[Comment]:
        """List replies to a specific comment."""
        return self.list(parent=parent_id, **kwargs)

    def get_thread(self, post_id: int) -> dict[int, list[Comment]]:
        """Get comments organized by parent for threading."""
        all_comments = list(self.iterate_all(post=post_id))
        threads: dict[int, list[Comment]] = {}
        for comment in all_comments:
            parent = comment.parent
            if parent not in threads:
                threads[parent] = []
            threads[parent].append(comment)
        return threads
