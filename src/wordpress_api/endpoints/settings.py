"""Settings endpoint."""

from typing import Any

from ..models.settings import Settings
from .base import BaseEndpoint


class SettingsEndpoint(BaseEndpoint):
    """Endpoint for managing WordPress site settings."""

    _path = "/wp/v2/settings"

    def get(self) -> Settings:
        """Get all site settings."""
        response = self._get(self._path)
        return Settings.model_validate(response)

    def update(self, **settings: Any) -> Settings:
        """Update site settings.
        
        Args:
            **settings: Key-value pairs of settings to update.
        """
        response = self._post(self._path, data=settings)
        return Settings.model_validate(response)

    def get_title(self) -> str:
        """Get the site title."""
        settings = self.get()
        return settings.title

    def set_title(self, title: str) -> Settings:
        """Set the site title."""
        return self.update(title=title)

    def get_description(self) -> str:
        """Get the site description (tagline)."""
        settings = self.get()
        return settings.description

    def set_description(self, description: str) -> Settings:
        """Set the site description (tagline)."""
        return self.update(description=description)

    def get_timezone(self) -> str:
        """Get the site timezone."""
        settings = self.get()
        return settings.timezone

    def set_timezone(self, timezone: str) -> Settings:
        """Set the site timezone."""
        return self.update(timezone=timezone)
