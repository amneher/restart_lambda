"""Main WordPress REST API Client."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import httpx

from .auth import AuthHandler, ApplicationPasswordAuth, BasicAuth, JWTAuth
from .exceptions import raise_for_status, WordPressError
from .endpoints.posts import PostsEndpoint
from .endpoints.pages import PagesEndpoint
from .endpoints.media import MediaEndpoint
from .endpoints.users import UsersEndpoint
from .endpoints.comments import CommentsEndpoint
from .endpoints.categories import CategoriesEndpoint
from .endpoints.tags import TagsEndpoint
from .endpoints.taxonomies import TaxonomiesEndpoint
from .endpoints.settings import SettingsEndpoint
from .endpoints.plugins import PluginsEndpoint
from .endpoints.themes import ThemesEndpoint
from .endpoints.menus import MenusEndpoint
from .endpoints.search import SearchEndpoint
from .endpoints.blocks import BlocksEndpoint
from .endpoints.revisions import RevisionsEndpoint
from .endpoints.autosaves import AutosavesEndpoint
from .endpoints.post_types import PostTypesEndpoint
from .endpoints.statuses import StatusesEndpoint
from .endpoints.application_passwords import ApplicationPasswordsEndpoint


class WordPressClient:
    """WordPress REST API Client.
    
    A full-featured Python interface to the WordPress REST API.
    
    Example:
        ```python
        from wordpress_api import WordPressClient, ApplicationPasswordAuth
        
        auth = ApplicationPasswordAuth("username", "xxxx xxxx xxxx xxxx xxxx xxxx")
        client = WordPressClient("https://example.com", auth=auth)
        
        # List posts
        posts = client.posts.list()
        
        # Create a new post
        new_post = client.posts.create({
            "title": "Hello World",
            "content": "This is my first post!",
            "status": "publish"
        })
        
        # Get current user
        me = client.users.me()
        ```
    
    Args:
        base_url: The WordPress site URL (e.g., "https://example.com").
        auth: Authentication handler (ApplicationPasswordAuth, BasicAuth, or JWTAuth).
        timeout: Request timeout in seconds (default 30).
        verify_ssl: Whether to verify SSL certificates (default True).
        user_agent: Custom User-Agent string.
        api_prefix: REST API prefix (default "/wp-json").
    """

    def __init__(
        self,
        base_url: str,
        auth: AuthHandler | None = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        user_agent: str | None = None,
        api_prefix: str = "/wp-json",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_prefix = api_prefix
        self.auth = auth
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if user_agent:
            headers["User-Agent"] = user_agent
        else:
            headers["User-Agent"] = "WordPress-Python-Client/1.0"
        
        if auth:
            headers.update(auth.get_headers())
        
        self._client = httpx.Client(
            base_url=f"{self.base_url}{self.api_prefix}",
            headers=headers,
            timeout=timeout,
            verify=verify_ssl,
        )
        
        self._last_response: httpx.Response | None = None
        self._total_pages: int | None = None
        self._total_items: int | None = None
        
        self._init_endpoints()

    def _init_endpoints(self) -> None:
        """Initialize all API endpoints."""
        self.posts = PostsEndpoint(self)
        self.pages = PagesEndpoint(self)
        self.media = MediaEndpoint(self)
        self.users = UsersEndpoint(self)
        self.comments = CommentsEndpoint(self)
        self.categories = CategoriesEndpoint(self)
        self.tags = TagsEndpoint(self)
        self.taxonomies = TaxonomiesEndpoint(self)
        self.settings = SettingsEndpoint(self)
        self.plugins = PluginsEndpoint(self)
        self.themes = ThemesEndpoint(self)
        self.menus = MenusEndpoint(self)
        self.search = SearchEndpoint(self)
        self.blocks = BlocksEndpoint(self)
        self.revisions = RevisionsEndpoint(self)
        self.autosaves = AutosavesEndpoint(self)
        self.post_types = PostTypesEndpoint(self)
        self.statuses = StatusesEndpoint(self)
        self.application_passwords = ApplicationPasswordsEndpoint(self)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Make an HTTP request to the WordPress REST API."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        if content is not None:
            response = self._client.request(
                method,
                path,
                params=params,
                content=content,
                headers=request_headers,
            )
        elif files:
            response = self._client.request(
                method,
                path,
                params=params,
                files=files,
                headers=request_headers,
            )
        else:
            response = self._client.request(
                method,
                path,
                params=params,
                json=json,
                headers=request_headers,
            )
        
        self._last_response = response
        self._total_pages = int(response.headers.get("X-WP-TotalPages", 0))
        self._total_items = int(response.headers.get("X-WP-Total", 0))
        
        if response.status_code >= 400:
            try:
                error_data = response.json()
            except Exception:
                error_data = {"message": response.text}
            raise_for_status(response.status_code, error_data)
        
        if response.status_code == 204:
            return {}
        
        try:
            return response.json()
        except Exception:
            return {"raw": response.text}

    def discover(self) -> dict[str, Any]:
        """Discover the WordPress REST API.
        
        Returns information about available routes and authentication.
        """
        return self._request("GET", "/")

    def get_namespaces(self) -> list[str]:
        """Get available API namespaces."""
        discovery = self.discover()
        return discovery.get("namespaces", [])

    def get_routes(self) -> dict[str, Any]:
        """Get all available API routes."""
        discovery = self.discover()
        return discovery.get("routes", {})

    def get_authentication_status(self) -> dict[str, Any]:
        """Check if the current authentication is valid."""
        discovery = self.discover()
        return discovery.get("authentication", {})

    @property
    def total_pages(self) -> int | None:
        """Total pages from the last list request."""
        return self._total_pages

    @property
    def total_items(self) -> int | None:
        """Total items from the last list request."""
        return self._total_items

    @property
    def last_response(self) -> httpx.Response | None:
        """The last HTTP response received."""
        return self._last_response

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "WordPressClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def custom_post_type(self, post_type: str) -> "CustomPostTypeEndpoint":
        """Access a custom post type endpoint.
        
        Args:
            post_type: The custom post type slug (e.g., "products", "portfolio").
        
        Returns:
            A CustomPostTypeEndpoint instance for the specified post type.
        """
        return CustomPostTypeEndpoint(self, post_type)


class CustomPostTypeEndpoint:
    """Endpoint for custom post types."""

    def __init__(self, client: WordPressClient, post_type: str) -> None:
        self._client = client
        self.post_type = post_type
        self._path = f"/wp/v2/{post_type}"

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._client._request("GET", path, params=params)

    def _post(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return self._client._request("POST", path, json=data)

    def _delete(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._client._request("DELETE", path, params=params)

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """List items of this custom post type."""
        params = {"page": page, "per_page": per_page, **kwargs}
        return self._get(self._path, params=params)

    def get(self, id: int, **kwargs: Any) -> dict[str, Any]:
        """Get a single item by ID."""
        return self._get(f"{self._path}/{id}", params=kwargs)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new item."""
        return self._post(self._path, data=data)

    def update(self, id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing item."""
        return self._post(f"{self._path}/{id}", data=data)

    def delete(self, id: int, force: bool = False, **kwargs: Any) -> dict[str, Any]:
        """Delete an item."""
        params = {"force": force, **kwargs}
        return self._delete(f"{self._path}/{id}", params=params)
