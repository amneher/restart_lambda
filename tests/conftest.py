"""Pytest fixtures for WordPress API tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import respx
import httpx

from wordpress_api import WordPressClient, ApplicationPasswordAuth, BasicAuth, JWTAuth


@pytest.fixture
def base_url():
    """Return the test WordPress site URL."""
    return "https://example.com"


@pytest.fixture
def api_url(base_url):
    """Return the full API URL."""
    return f"{base_url}/wp-json"


@pytest.fixture
def mock_auth():
    """Return a mock authentication handler."""
    return ApplicationPasswordAuth("testuser", "xxxx xxxx xxxx xxxx")


@pytest.fixture
def client(base_url, mock_auth):
    """Return a WordPress client for testing."""
    return WordPressClient(base_url, auth=mock_auth)


@pytest.fixture
def unauthenticated_client(base_url):
    """Return a WordPress client without authentication."""
    return WordPressClient(base_url)


@pytest.fixture
def mock_post():
    """Return mock post data."""
    return {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "date_gmt": "2024-01-15T10:30:00",
        "guid": {"rendered": "https://example.com/?p=1"},
        "modified": "2024-01-15T10:30:00",
        "modified_gmt": "2024-01-15T10:30:00",
        "slug": "hello-world",
        "status": "publish",
        "type": "post",
        "link": "https://example.com/hello-world/",
        "title": {"rendered": "Hello World"},
        "content": {"rendered": "<p>Hello World content</p>"},
        "excerpt": {"rendered": "<p>Hello World excerpt</p>"},
        "author": 1,
        "featured_media": 0,
        "comment_status": "open",
        "ping_status": "open",
        "sticky": False,
        "template": "",
        "format": "standard",
        "meta": {},
        "categories": [1],
        "tags": [],
    }


@pytest.fixture
def mock_page():
    """Return mock page data."""
    return {
        "id": 10,
        "date": "2024-01-15T10:30:00",
        "date_gmt": "2024-01-15T10:30:00",
        "guid": {"rendered": "https://example.com/?page_id=10"},
        "modified": "2024-01-15T10:30:00",
        "modified_gmt": "2024-01-15T10:30:00",
        "slug": "about",
        "status": "publish",
        "type": "page",
        "link": "https://example.com/about/",
        "title": {"rendered": "About Us"},
        "content": {"rendered": "<p>About us content</p>"},
        "excerpt": {"rendered": ""},
        "author": 1,
        "featured_media": 0,
        "parent": 0,
        "menu_order": 0,
        "comment_status": "closed",
        "ping_status": "closed",
        "template": "",
        "meta": {},
    }


@pytest.fixture
def mock_user():
    """Return mock user data."""
    return {
        "id": 1,
        "username": "admin",
        "name": "Admin User",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "url": "https://example.com",
        "description": "Site administrator",
        "link": "https://example.com/author/admin/",
        "locale": "en_US",
        "nickname": "admin",
        "slug": "admin",
        "registered_date": "2024-01-01T00:00:00",
        "roles": ["administrator"],
        "capabilities": {"administrator": True},
        "extra_capabilities": {},
        "avatar_urls": {"24": "https://example.com/avatar.jpg"},
        "meta": {},
    }


@pytest.fixture
def mock_category():
    """Return mock category data."""
    return {
        "id": 1,
        "count": 5,
        "description": "Default category",
        "link": "https://example.com/category/uncategorized/",
        "name": "Uncategorized",
        "slug": "uncategorized",
        "taxonomy": "category",
        "parent": 0,
        "meta": {},
    }


@pytest.fixture
def mock_tag():
    """Return mock tag data."""
    return {
        "id": 1,
        "count": 3,
        "description": "",
        "link": "https://example.com/tag/python/",
        "name": "Python",
        "slug": "python",
        "taxonomy": "post_tag",
        "meta": {},
    }


@pytest.fixture
def mock_comment():
    """Return mock comment data."""
    return {
        "id": 1,
        "post": 1,
        "parent": 0,
        "author": 0,
        "author_name": "John Doe",
        "author_email": "john@example.com",
        "author_url": "",
        "author_ip": "127.0.0.1",
        "author_user_agent": "Mozilla/5.0",
        "date": "2024-01-15T10:30:00",
        "date_gmt": "2024-01-15T10:30:00",
        "content": {"rendered": "<p>Great post!</p>"},
        "link": "https://example.com/hello-world/#comment-1",
        "status": "approved",
        "type": "comment",
        "author_avatar_urls": {},
        "meta": {},
    }


@pytest.fixture
def mock_media():
    """Return mock media data."""
    return {
        "id": 100,
        "date": "2024-01-15T10:30:00",
        "date_gmt": "2024-01-15T10:30:00",
        "guid": {"rendered": "https://example.com/wp-content/uploads/image.jpg"},
        "modified": "2024-01-15T10:30:00",
        "modified_gmt": "2024-01-15T10:30:00",
        "slug": "image",
        "status": "inherit",
        "type": "attachment",
        "link": "https://example.com/image/",
        "title": {"rendered": "Test Image"},
        "author": 1,
        "comment_status": "open",
        "ping_status": "closed",
        "template": "",
        "meta": {},
        "description": {"rendered": ""},
        "caption": {"rendered": ""},
        "alt_text": "Test image alt",
        "media_type": "image",
        "mime_type": "image/jpeg",
        "media_details": {
            "width": 1920,
            "height": 1080,
            "file": "2024/01/image.jpg",
            "filesize": 102400,
            "sizes": {},
            "image_meta": {},
        },
        "post": None,
        "source_url": "https://example.com/wp-content/uploads/image.jpg",
    }


@pytest.fixture
def mock_application_password():
    """Return mock application password data."""
    return {
        "uuid": "12345678-1234-1234-1234-123456789012",
        "app_id": "",
        "name": "Test App",
        "created": "2024-01-15T10:30:00",
        "last_used": None,
        "last_ip": None,
    }


@pytest.fixture
def mock_application_password_created():
    """Return mock created application password data (includes password)."""
    return {
        "uuid": "12345678-1234-1234-1234-123456789012",
        "app_id": "",
        "name": "Test App",
        "created": "2024-01-15T10:30:00",
        "password": "abcd efgh ijkl mnop",
    }
