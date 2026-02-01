"""Base endpoint class."""

from __future__ import annotations

from typing import Any, TypeVar, Generic, TYPE_CHECKING
from collections.abc import Iterator

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseEndpoint:
    """Base class for all API endpoints."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make GET request."""
        return self._client._request("GET", path, params=params)

    def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Any:
        """Make POST request."""
        return self._client._request("POST", path, json=data, files=files)

    def _put(self, path: str, data: dict[str, Any] | None = None) -> Any:
        """Make PUT request."""
        return self._client._request("PUT", path, json=data)

    def _patch(self, path: str, data: dict[str, Any] | None = None) -> Any:
        """Make PATCH request."""
        return self._client._request("PATCH", path, json=data)

    def _delete(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make DELETE request."""
        return self._client._request("DELETE", path, params=params)


class CRUDEndpoint(BaseEndpoint, Generic[T]):
    """Base class for CRUD endpoints."""

    _path: str = ""
    _model_class: type[T]

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "desc",
        orderby: str = "date",
        **kwargs: Any,
    ) -> list[T]:
        """List resources with pagination."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        if search:
            params["search"] = search
        params.update(kwargs)

        response = self._get(self._path, params=params)
        return [self._model_class.model_validate(item) for item in response]

    def get(self, id: int, context: str = "view", **kwargs: Any) -> T:
        """Get a single resource by ID."""
        params = {"context": context, **kwargs}
        response = self._get(f"{self._path}/{id}", params=params)
        return self._model_class.model_validate(response)

    def create(self, data: BaseModel | dict[str, Any]) -> T:
        """Create a new resource."""
        if isinstance(data, BaseModel):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        response = self._post(self._path, data=payload)
        return self._model_class.model_validate(response)

    def update(self, id: int, data: BaseModel | dict[str, Any]) -> T:
        """Update an existing resource."""
        if isinstance(data, BaseModel):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        response = self._post(f"{self._path}/{id}", data=payload)
        return self._model_class.model_validate(response)

    def delete(self, id: int, force: bool = False, **kwargs: Any) -> dict[str, Any]:
        """Delete a resource."""
        params = {"force": force, **kwargs}
        return self._delete(f"{self._path}/{id}", params=params)

    def iterate_all(
        self,
        per_page: int = 100,
        **kwargs: Any,
    ) -> Iterator[T]:
        """Iterate through all resources with automatic pagination."""
        page = 1
        while True:
            items = self.list(page=page, per_page=per_page, **kwargs)
            if not items:
                break
            yield from items
            if len(items) < per_page:
                break
            page += 1
