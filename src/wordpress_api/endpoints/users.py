"""Users endpoint."""

from __future__ import annotations

from typing import Any

from ..models.user import User, UserCreate, UserUpdate
from .base import CRUDEndpoint


class UsersEndpoint(CRUDEndpoint[User]):
    """Endpoint for managing WordPress users."""

    _path = "/wp/v2/users"
    _model_class = User

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "asc",
        orderby: str = "name",
        roles: str | list[str] | None = None,
        capabilities: str | list[str] | None = None,
        who: str | None = None,
        has_published_posts: bool | str | list[str] | None = None,
        slug: str | list[str] | None = None,
        include: list[int] | None = None,
        exclude: list[int] | None = None,
        **kwargs: Any,
    ) -> list[User]:
        """List users with filtering options."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        
        if search:
            params["search"] = search
        if roles:
            if isinstance(roles, list):
                params["roles"] = ",".join(roles)
            else:
                params["roles"] = roles
        if capabilities:
            if isinstance(capabilities, list):
                params["capabilities"] = ",".join(capabilities)
            else:
                params["capabilities"] = capabilities
        if who:
            params["who"] = who
        if has_published_posts is not None:
            if isinstance(has_published_posts, bool):
                params["has_published_posts"] = has_published_posts
            elif isinstance(has_published_posts, list):
                params["has_published_posts"] = ",".join(has_published_posts)
            else:
                params["has_published_posts"] = has_published_posts
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
        return [User.model_validate(item) for item in response]

    def create(self, data: UserCreate | dict[str, Any]) -> User:
        """Create a new user."""
        return super().create(data)

    def update(self, id: int, data: UserUpdate | dict[str, Any]) -> User:
        """Update an existing user."""
        return super().update(id, data)

    def me(self, context: str = "view") -> User:
        """Get the current authenticated user."""
        response = self._get(f"{self._path}/me", params={"context": context})
        return User.model_validate(response)

    def update_me(self, data: UserUpdate | dict[str, Any]) -> User:
        """Update the current authenticated user."""
        if isinstance(data, UserUpdate):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        response = self._post(f"{self._path}/me", data=payload)
        return User.model_validate(response)

    def delete(
        self,
        id: int,
        force: bool = True,
        reassign: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Delete a user.
        
        Args:
            id: User ID to delete.
            force: Must be true (users cannot be trashed).
            reassign: Reassign posts to this user ID.
        """
        params = {"force": force}
        if reassign is not None:
            params["reassign"] = reassign
        params.update(kwargs)
        return self._delete(f"{self._path}/{id}", params=params)

    def get_by_slug(self, slug: str) -> User | None:
        """Get a user by their slug."""
        users = self.list(slug=slug)
        return users[0] if users else None

    def list_authors(self, **kwargs: Any) -> list[User]:
        """List users who have published posts."""
        return self.list(has_published_posts=True, **kwargs)

    def list_by_role(self, role: str, **kwargs: Any) -> list[User]:
        """List users with a specific role."""
        return self.list(roles=role, **kwargs)
