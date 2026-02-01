"""Tests for WordPress client."""

import pytest
import respx
import httpx

from wordpress_api import WordPressClient, ApplicationPasswordAuth


class TestWordPressClient:
    """Tests for WordPressClient class."""

    def test_init_with_auth(self, base_url, mock_auth):
        """Test client initialization with auth."""
        client = WordPressClient(base_url, auth=mock_auth)
        assert client.base_url == base_url
        assert client.auth == mock_auth

    def test_init_without_auth(self, base_url):
        """Test client initialization without auth."""
        client = WordPressClient(base_url)
        assert client.base_url == base_url
        assert client.auth is None

    def test_init_with_custom_timeout(self, base_url):
        """Test client initialization with custom timeout."""
        client = WordPressClient(base_url, timeout=60.0)
        assert client.timeout == 60.0

    def test_init_with_custom_user_agent(self, base_url):
        """Test client initialization with custom user agent."""
        client = WordPressClient(base_url, user_agent="MyApp/1.0")
        assert "MyApp/1.0" in client._client.headers["User-Agent"]

    def test_init_trailing_slash_removed(self):
        """Test that trailing slash is removed from base URL."""
        client = WordPressClient("https://example.com/")
        assert client.base_url == "https://example.com"

    def test_endpoints_initialized(self, client):
        """Test that all endpoints are initialized."""
        assert hasattr(client, "posts")
        assert hasattr(client, "pages")
        assert hasattr(client, "media")
        assert hasattr(client, "users")
        assert hasattr(client, "comments")
        assert hasattr(client, "categories")
        assert hasattr(client, "tags")
        assert hasattr(client, "taxonomies")
        assert hasattr(client, "settings")
        assert hasattr(client, "plugins")
        assert hasattr(client, "themes")
        assert hasattr(client, "menus")
        assert hasattr(client, "search")
        assert hasattr(client, "blocks")
        assert hasattr(client, "revisions")
        assert hasattr(client, "autosaves")
        assert hasattr(client, "post_types")
        assert hasattr(client, "statuses")
        assert hasattr(client, "application_passwords")

    def test_context_manager(self, base_url, mock_auth):
        """Test client as context manager."""
        with WordPressClient(base_url, auth=mock_auth) as client:
            assert client is not None

    def test_custom_post_type(self, client):
        """Test custom post type endpoint creation."""
        products = client.custom_post_type("products")
        assert products.post_type == "products"
        assert products._path == "/wp/v2/products"

    @respx.mock
    def test_discover(self, client, api_url):
        """Test API discovery."""
        respx.get(f"{api_url}/").mock(return_value=httpx.Response(200, json={
            "name": "My Site",
            "namespaces": ["wp/v2"],
            "routes": {"/wp/v2/posts": {}},
        }))
        
        result = client.discover()
        assert "name" in result
        assert "namespaces" in result

    @respx.mock
    def test_get_namespaces(self, client, api_url):
        """Test getting API namespaces."""
        respx.get(f"{api_url}/").mock(return_value=httpx.Response(200, json={
            "namespaces": ["wp/v2", "wp/v2/oembed"],
        }))
        
        namespaces = client.get_namespaces()
        assert "wp/v2" in namespaces

    @respx.mock
    def test_request_stores_pagination(self, client, api_url, mock_post):
        """Test that pagination headers are stored."""
        respx.get(f"{api_url}/wp/v2/posts").mock(return_value=httpx.Response(
            200,
            json=[mock_post],
            headers={"X-WP-Total": "100", "X-WP-TotalPages": "10"},
        ))
        
        client.posts.list()
        assert client.total_items == 100
        assert client.total_pages == 10

    @respx.mock
    def test_error_handling(self, client, api_url):
        """Test that errors are properly raised."""
        from wordpress_api.exceptions import NotFoundError
        
        respx.get(f"{api_url}/wp/v2/posts/99999").mock(return_value=httpx.Response(
            404,
            json={"code": "rest_post_invalid_id", "message": "Invalid post ID."},
        ))
        
        with pytest.raises(NotFoundError):
            client.posts.get(99999)
