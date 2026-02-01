"""Categories endpoint."""

from __future__ import annotations

from typing import Any

from ..models.category import Category, CategoryCreate, CategoryUpdate
from .base import CRUDEndpoint


class CategoriesEndpoint(CRUDEndpoint[Category]):
    """Endpoint for managing WordPress categories."""

    _path = "/wp/v2/categories"
    _model_class = Category

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "asc",
        orderby: str = "name",
        hide_empty: bool = False,
        parent: int | None = None,
        post: int | None = None,
        slug: str | list[str] | None = None,
        include: list[int] | None = None,
        exclude: list[int] | None = None,
        **kwargs: Any,
    ) -> list[Category]:
        """List categories with filtering options."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
            "hide_empty": hide_empty,
        }
        
        if search:
            params["search"] = search
        if parent is not None:
            params["parent"] = parent
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
        return [Category.model_validate(item) for item in response]

    def create(self, data: CategoryCreate | dict[str, Any]) -> Category:
        """Create a new category."""
        return super().create(data)

    def update(self, id: int, data: CategoryUpdate | dict[str, Any]) -> Category:
        """Update an existing category."""
        return super().update(id, data)

    def get_by_slug(self, slug: str) -> Category | None:
        """Get a category by its slug."""
        categories = self.list(slug=slug)
        return categories[0] if categories else None

    def get_children(self, parent_id: int, **kwargs: Any) -> list[Category]:
        """Get child categories of a parent."""
        return self.list(parent=parent_id, **kwargs)

    def get_hierarchy(self) -> dict[int, list[Category]]:
        """Get all categories organized by parent ID."""
        all_categories = list(self.iterate_all())
        hierarchy: dict[int, list[Category]] = {}
        for category in all_categories:
            parent = category.parent
            if parent not in hierarchy:
                hierarchy[parent] = []
            hierarchy[parent].append(category)
        return hierarchy

    def get_for_post(self, post_id: int) -> list[Category]:
        """Get categories assigned to a specific post."""
        return self.list(post=post_id)
