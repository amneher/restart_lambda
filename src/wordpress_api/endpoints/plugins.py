"""Plugins endpoint."""

from __future__ import annotations

from typing import Any

from ..models.plugin import Plugin
from .base import BaseEndpoint


class PluginsEndpoint(BaseEndpoint):
    """Endpoint for managing WordPress plugins."""

    _path = "/wp/v2/plugins"

    def list(
        self,
        search: str | None = None,
        status: str | None = None,
        **kwargs: Any,
    ) -> list[Plugin]:
        """List installed plugins.
        
        Args:
            search: Limit results to those matching a string.
            status: Filter by plugin status (active, inactive).
        """
        params: dict[str, Any] = {}
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        params.update(kwargs)
        
        response = self._get(self._path, params=params)
        return [Plugin.model_validate(item) for item in response]

    def get(self, plugin: str, **kwargs: Any) -> Plugin:
        """Get a specific plugin.
        
        Args:
            plugin: Plugin identifier (folder/file format, e.g., "akismet/akismet").
        """
        encoded_plugin = plugin.replace("/", "%2F")
        response = self._get(f"{self._path}/{encoded_plugin}", params=kwargs)
        return Plugin.model_validate(response)

    def activate(self, plugin: str) -> Plugin:
        """Activate a plugin.
        
        Args:
            plugin: Plugin identifier (folder/file format).
        """
        encoded_plugin = plugin.replace("/", "%2F")
        response = self._post(
            f"{self._path}/{encoded_plugin}",
            data={"status": "active"},
        )
        return Plugin.model_validate(response)

    def deactivate(self, plugin: str) -> Plugin:
        """Deactivate a plugin.
        
        Args:
            plugin: Plugin identifier (folder/file format).
        """
        encoded_plugin = plugin.replace("/", "%2F")
        response = self._post(
            f"{self._path}/{encoded_plugin}",
            data={"status": "inactive"},
        )
        return Plugin.model_validate(response)

    def delete(self, plugin: str) -> dict[str, Any]:
        """Delete a plugin.
        
        Args:
            plugin: Plugin identifier (folder/file format).
        """
        encoded_plugin = plugin.replace("/", "%2F")
        return self._delete(f"{self._path}/{encoded_plugin}")

    def list_active(self) -> list[Plugin]:
        """List all active plugins."""
        return self.list(status="active")

    def list_inactive(self) -> list[Plugin]:
        """List all inactive plugins."""
        return self.list(status="inactive")
