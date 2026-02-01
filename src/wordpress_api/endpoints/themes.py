"""Themes endpoint."""

from __future__ import annotations

from typing import Any

from ..models.theme import Theme
from .base import BaseEndpoint


class ThemesEndpoint(BaseEndpoint):
    """Endpoint for managing WordPress themes."""

    _path = "/wp/v2/themes"

    def list(self, status: str | list[str] | None = None, **kwargs: Any) -> list[Theme]:
        """List installed themes.
        
        Args:
            status: Filter by theme status (active, inactive).
        """
        params: dict[str, Any] = {}
        if status:
            if isinstance(status, list):
                params["status"] = ",".join(status)
            else:
                params["status"] = status
        params.update(kwargs)
        
        response = self._get(self._path, params=params)
        return [Theme.model_validate(item) for item in response]

    def get(self, stylesheet: str, **kwargs: Any) -> Theme:
        """Get a specific theme.
        
        Args:
            stylesheet: Theme stylesheet name.
        """
        response = self._get(f"{self._path}/{stylesheet}", params=kwargs)
        return Theme.model_validate(response)

    def get_active(self) -> Theme:
        """Get the currently active theme."""
        themes = self.list(status="active")
        if themes:
            return themes[0]
        raise ValueError("No active theme found")

    def list_inactive(self) -> list[Theme]:
        """List all inactive themes."""
        return self.list(status="inactive")
