"""Application Passwords endpoint."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..models.base import parse_datetime
from .base import BaseEndpoint


class ApplicationPassword(BaseModel):
    """WordPress Application Password object."""

    uuid: str = ""
    app_id: str = ""
    name: str = ""
    created: datetime | None = None
    last_used: datetime | None = None
    last_ip: str | None = None

    @field_validator("created", "last_used", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class ApplicationPasswordCreated(BaseModel):
    """Response when creating an Application Password (includes the password)."""

    uuid: str = ""
    app_id: str = ""
    name: str = ""
    created: datetime | None = None
    password: str = ""

    @field_validator("created", mode="before")
    @classmethod
    def parse_dates(cls, v: Any) -> datetime | None:
        return parse_datetime(v)


class ApplicationPasswordsEndpoint(BaseEndpoint):
    """Endpoint for managing WordPress Application Passwords.
    
    Application Passwords were introduced in WordPress 5.6 and provide
    a secure way to authenticate REST API requests.
    """

    def _get_path(self, user_id: int | str) -> str:
        """Get the endpoint path for a user's application passwords."""
        return f"/wp/v2/users/{user_id}/application-passwords"

    def list(self, user_id: int | str = "me") -> list[ApplicationPassword]:
        """List all application passwords for a user.
        
        Args:
            user_id: User ID or "me" for current user.
        
        Returns:
            List of application passwords (without the actual password values).
        """
        response = self._get(self._get_path(user_id))
        return [ApplicationPassword.model_validate(item) for item in response]

    def get(self, uuid: str, user_id: int | str = "me") -> ApplicationPassword:
        """Get a specific application password by UUID.
        
        Args:
            uuid: The UUID of the application password.
            user_id: User ID or "me" for current user.
        
        Returns:
            The application password details.
        """
        response = self._get(f"{self._get_path(user_id)}/{uuid}")
        return ApplicationPassword.model_validate(response)

    def create(
        self,
        name: str,
        user_id: int | str = "me",
        app_id: str | None = None,
    ) -> ApplicationPasswordCreated:
        """Create a new application password.
        
        Args:
            name: A human-readable name for the application password.
            user_id: User ID or "me" for current user.
            app_id: Optional application identifier (UUID format).
        
        Returns:
            The created application password including the password value.
            Note: The password is only returned once at creation time!
        """
        data: dict[str, Any] = {"name": name}
        if app_id:
            data["app_id"] = app_id
        
        response = self._post(self._get_path(user_id), data=data)
        return ApplicationPasswordCreated.model_validate(response)

    def update(
        self,
        uuid: str,
        name: str,
        user_id: int | str = "me",
    ) -> ApplicationPassword:
        """Update an application password's name.
        
        Args:
            uuid: The UUID of the application password.
            name: The new name for the application password.
            user_id: User ID or "me" for current user.
        
        Returns:
            The updated application password.
        """
        response = self._post(
            f"{self._get_path(user_id)}/{uuid}",
            data={"name": name},
        )
        return ApplicationPassword.model_validate(response)

    def delete(
        self,
        uuid: str,
        user_id: int | str = "me",
    ) -> dict[str, Any]:
        """Delete an application password.
        
        Args:
            uuid: The UUID of the application password.
            user_id: User ID or "me" for current user.
        
        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self._get_path(user_id)}/{uuid}")

    def delete_all(self, user_id: int | str = "me") -> dict[str, Any]:
        """Delete all application passwords for a user.
        
        Args:
            user_id: User ID or "me" for current user.
        
        Returns:
            Deletion confirmation.
        """
        return self._delete(self._get_path(user_id))

    def get_or_create(
        self,
        name: str,
        user_id: int | str = "me",
        app_id: str | None = None,
    ) -> ApplicationPasswordCreated | ApplicationPassword:
        """Get an existing application password by name, or create one if none exist.
        
        This method checks if the user has any application passwords with the
        given name. If found, it returns the existing one. If not found (or if
        no application passwords exist), it creates a new one.
        
        Args:
            name: The name to search for or use when creating.
            user_id: User ID or "me" for current user.
            app_id: Optional application identifier for new passwords.
        
        Returns:
            Either an existing ApplicationPassword or a newly created
            ApplicationPasswordCreated (which includes the password value).
        
        Note:
            If an existing password is returned, the actual password value
            is NOT included (WordPress doesn't store or return it after creation).
            Only newly created passwords include the password value.
        """
        existing = self.list(user_id)
        
        for app_pass in existing:
            if app_pass.name == name:
                return app_pass
        
        return self.create(name=name, user_id=user_id, app_id=app_id)

    def ensure_exists(
        self,
        name: str,
        user_id: int | str = "me",
        app_id: str | None = None,
    ) -> tuple[ApplicationPasswordCreated | ApplicationPassword, bool]:
        """Ensure an application password exists, creating if necessary.
        
        Args:
            name: The name for the application password.
            user_id: User ID or "me" for current user.
            app_id: Optional application identifier for new passwords.
        
        Returns:
            A tuple of (application_password, was_created).
            If was_created is True, the password value is available.
        """
        existing = self.list(user_id)
        
        for app_pass in existing:
            if app_pass.name == name:
                return app_pass, False
        
        new_password = self.create(name=name, user_id=user_id, app_id=app_id)
        return new_password, True

    def has_any(self, user_id: int | str = "me") -> bool:
        """Check if the user has any application passwords.
        
        Args:
            user_id: User ID or "me" for current user.
        
        Returns:
            True if the user has at least one application password.
        """
        return len(self.list(user_id)) > 0

    def count(self, user_id: int | str = "me") -> int:
        """Count the number of application passwords for a user.
        
        Args:
            user_id: User ID or "me" for current user.
        
        Returns:
            Number of application passwords.
        """
        return len(self.list(user_id))
