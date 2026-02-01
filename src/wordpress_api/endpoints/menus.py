"""Menus endpoint."""

from __future__ import annotations

from typing import Any

from ..models.menu import Menu, MenuItem, MenuItemCreate, MenuItemUpdate
from .base import BaseEndpoint


class MenusEndpoint(BaseEndpoint):
    """Endpoint for managing WordPress navigation menus."""

    _menus_path = "/wp/v2/menus"
    _items_path = "/wp/v2/menu-items"
    _locations_path = "/wp/v2/menu-locations"

    def list_menus(
        self,
        page: int = 1,
        per_page: int = 100,
        search: str | None = None,
        **kwargs: Any,
    ) -> list[Menu]:
        """List navigation menus."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        if search:
            params["search"] = search
        params.update(kwargs)
        
        response = self._get(self._menus_path, params=params)
        return [Menu.model_validate(item) for item in response]

    def get_menu(self, id: int) -> Menu:
        """Get a specific menu by ID."""
        response = self._get(f"{self._menus_path}/{id}")
        return Menu.model_validate(response)

    def create_menu(self, name: str, **kwargs: Any) -> Menu:
        """Create a new menu."""
        data = {"name": name, **kwargs}
        response = self._post(self._menus_path, data=data)
        return Menu.model_validate(response)

    def update_menu(self, id: int, **kwargs: Any) -> Menu:
        """Update a menu."""
        response = self._post(f"{self._menus_path}/{id}", data=kwargs)
        return Menu.model_validate(response)

    def delete_menu(self, id: int, force: bool = True) -> dict[str, Any]:
        """Delete a menu."""
        return self._delete(f"{self._menus_path}/{id}", params={"force": force})

    def list_items(
        self,
        menus: int | list[int] | None = None,
        page: int = 1,
        per_page: int = 100,
        order: str = "asc",
        orderby: str = "menu_order",
        **kwargs: Any,
    ) -> list[MenuItem]:
        """List menu items."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        if menus is not None:
            if isinstance(menus, list):
                params["menus"] = ",".join(map(str, menus))
            else:
                params["menus"] = menus
        params.update(kwargs)
        
        response = self._get(self._items_path, params=params)
        return [MenuItem.model_validate(item) for item in response]

    def get_item(self, id: int) -> MenuItem:
        """Get a specific menu item."""
        response = self._get(f"{self._items_path}/{id}")
        return MenuItem.model_validate(response)

    def create_item(self, data: MenuItemCreate | dict[str, Any]) -> MenuItem:
        """Create a new menu item."""
        if isinstance(data, MenuItemCreate):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        response = self._post(self._items_path, data=payload)
        return MenuItem.model_validate(response)

    def update_item(self, id: int, data: MenuItemUpdate | dict[str, Any]) -> MenuItem:
        """Update a menu item."""
        if isinstance(data, MenuItemUpdate):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        response = self._post(f"{self._items_path}/{id}", data=payload)
        return MenuItem.model_validate(response)

    def delete_item(self, id: int, force: bool = True) -> dict[str, Any]:
        """Delete a menu item."""
        return self._delete(f"{self._items_path}/{id}", params={"force": force})

    def list_locations(self) -> dict[str, Any]:
        """List registered menu locations."""
        return self._get(self._locations_path)

    def get_location(self, location: str) -> dict[str, Any]:
        """Get a specific menu location."""
        return self._get(f"{self._locations_path}/{location}")

    def get_menu_items(self, menu_id: int) -> list[MenuItem]:
        """Get all items for a specific menu."""
        return self.list_items(menus=menu_id)
