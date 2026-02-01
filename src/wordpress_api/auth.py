"""Authentication handlers for WordPress REST API."""

import base64
from abc import ABC, abstractmethod
from typing import Any

import httpx


class AuthHandler(ABC):
    """Abstract base class for authentication handlers."""

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        """Return headers required for authentication."""
        pass

    @abstractmethod
    def authenticate(self, request: httpx.Request) -> httpx.Request:
        """Authenticate the request."""
        pass


class BasicAuth(AuthHandler):
    """HTTP Basic Authentication.
    
    Note: Basic auth should only be used over HTTPS.
    """

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self._credentials = base64.b64encode(
            f"{username}:{password}".encode()
        ).decode()

    def get_headers(self) -> dict[str, str]:
        return {"Authorization": f"Basic {self._credentials}"}

    def authenticate(self, request: httpx.Request) -> httpx.Request:
        request.headers.update(self.get_headers())
        return request


class ApplicationPasswordAuth(AuthHandler):
    """WordPress Application Passwords authentication.
    
    Application Passwords were introduced in WordPress 5.6 and provide
    a secure way to authenticate REST API requests without exposing
    the user's main password.
    """

    def __init__(self, username: str, application_password: str) -> None:
        self.username = username
        self.application_password = application_password.replace(" ", "")
        self._credentials = base64.b64encode(
            f"{username}:{self.application_password}".encode()
        ).decode()

    def get_headers(self) -> dict[str, str]:
        return {"Authorization": f"Basic {self._credentials}"}

    def authenticate(self, request: httpx.Request) -> httpx.Request:
        request.headers.update(self.get_headers())
        return request


class JWTAuth(AuthHandler):
    """JWT (JSON Web Token) Authentication.
    
    Requires a JWT authentication plugin on the WordPress site.
    """

    def __init__(self, token: str | None = None) -> None:
        self.token = token
        self._base_url: str | None = None

    def set_base_url(self, url: str) -> None:
        """Set the base URL for token requests."""
        self._base_url = url

    def get_headers(self) -> dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def authenticate(self, request: httpx.Request) -> httpx.Request:
        if self.token:
            request.headers.update(self.get_headers())
        return request

    def obtain_token(
        self,
        client: httpx.Client,
        username: str,
        password: str,
        endpoint: str = "/wp-json/jwt-auth/v1/token",
    ) -> str:
        """Obtain a JWT token from the WordPress site."""
        response = client.post(
            endpoint,
            json={"username": username, "password": password},
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token", data.get("data", {}).get("token"))
        return self.token

    def validate_token(
        self,
        client: httpx.Client,
        endpoint: str = "/wp-json/jwt-auth/v1/token/validate",
    ) -> bool:
        """Validate the current JWT token."""
        if not self.token:
            return False
        response = client.post(endpoint, headers=self.get_headers())
        return response.status_code == 200


class OAuth2Auth(AuthHandler):
    """OAuth 2.0 Authentication.
    
    Requires OAuth 2.0 plugin on the WordPress site.
    """

    def __init__(
        self,
        access_token: str | None = None,
        refresh_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

    def get_headers(self) -> dict[str, str]:
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}

    def authenticate(self, request: httpx.Request) -> httpx.Request:
        if self.access_token:
            request.headers.update(self.get_headers())
        return request

    def refresh_access_token(
        self,
        client: httpx.Client,
        token_endpoint: str,
    ) -> str:
        """Refresh the access token using the refresh token."""
        if not self.refresh_token or not self.client_id:
            raise ValueError("Refresh token and client ID required")

        data: dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret

        response = client.post(token_endpoint, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        self.access_token = token_data["access_token"]
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
        
        return self.access_token
