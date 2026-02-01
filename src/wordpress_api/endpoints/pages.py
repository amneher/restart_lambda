"""Pages endpoint."""

from typing import Any

from ..models.page import Page, PageCreate, PageUpdate
from ..models.post import PostStatus
from .base import CRUDEndpoint


class PagesEndpoint(CRUDEndpoint[Page]):
    """Endpoint for managing WordPress pages."""

    _path = "/wp/v2/pages"
    _model_class = Page

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "asc",
        orderby: str = "menu_order",
        status: str | PostStatus | list[str] | None = None,
        parent: int | list[int] | None = None,
        parent_exclude: list[int] | None = None,
        author: int | list[int] | None = None,
        author_exclude: list[int] | None = None,
        before: str | None = None,
        after: str | None = None,
        menu_order: int | None = None,
        slug: str | list[str] | None = None,
        **kwargs: Any,
    ) -> list[Page]:
        """List pages with filtering options."""
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
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if menu_order is not None:
            params["menu_order"] = menu_order
        if slug:
            if isinstance(slug, list):
                params["slug"] = ",".join(slug)
            else:
                params["slug"] = slug

        params.update(kwargs)
        response = self._get(self._path, params=params)
        return [Page.model_validate(item) for item in response]

    def create(self, data: PageCreate | dict[str, Any]) -> Page:
        """Create a new page."""
        return super().create(data)

    def update(self, id: int, data: PageUpdate | dict[str, Any]) -> Page:
        """Update an existing page."""
        return super().update(id, data)

    def get_by_slug(self, slug: str) -> Page | None:
        """Get a page by its slug."""
        pages = self.list(slug=slug)
        return pages[0] if pages else None

    def get_children(self, parent_id: int, **kwargs: Any) -> list[Page]:
        """Get child pages of a parent page."""
        return self.list(parent=parent_id, **kwargs)

    def get_hierarchy(self) -> dict[int, list[Page]]:
        """Get all pages organized by parent ID."""
        all_pages = list(self.iterate_all())
        hierarchy: dict[int, list[Page]] = {}
        for page in all_pages:
            parent = page.parent
            if parent not in hierarchy:
                hierarchy[parent] = []
            hierarchy[parent].append(page)
        return hierarchy
