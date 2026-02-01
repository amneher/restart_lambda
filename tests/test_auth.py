"""Tests for authentication handlers."""

import base64
import pytest
import httpx

from wordpress_api.auth import (
    ApplicationPasswordAuth,
    BasicAuth,
    JWTAuth,
    OAuth2Auth,
)


class TestBasicAuth:
    """Tests for BasicAuth handler."""

    def test_init(self):
        """Test BasicAuth initialization."""
        auth = BasicAuth("user", "pass")
        assert auth.username == "user"
        assert auth.password == "pass"

    def test_get_headers(self):
        """Test that correct Authorization header is generated."""
        auth = BasicAuth("user", "pass")
        headers = auth.get_headers()
        
        expected = base64.b64encode(b"user:pass").decode()
        assert headers == {"Authorization": f"Basic {expected}"}

    def test_authenticate_request(self):
        """Test that request is authenticated correctly."""
        auth = BasicAuth("user", "pass")
        request = httpx.Request("GET", "https://example.com")
        
        authenticated = auth.authenticate(request)
        assert "Authorization" in authenticated.headers


class TestApplicationPasswordAuth:
    """Tests for ApplicationPasswordAuth handler."""

    def test_init(self):
        """Test ApplicationPasswordAuth initialization."""
        auth = ApplicationPasswordAuth("admin", "xxxx xxxx xxxx xxxx")
        assert auth.username == "admin"
        assert auth.application_password == "xxxxxxxxxxxxxxxx"

    def test_password_spaces_removed(self):
        """Test that spaces are removed from application password."""
        auth = ApplicationPasswordAuth("admin", "xxxx xxxx xxxx xxxx")
        assert " " not in auth.application_password

    def test_get_headers(self):
        """Test that correct Authorization header is generated."""
        auth = ApplicationPasswordAuth("admin", "testpassword")
        headers = auth.get_headers()
        
        expected = base64.b64encode(b"admin:testpassword").decode()
        assert headers == {"Authorization": f"Basic {expected}"}

    def test_authenticate_request(self):
        """Test that request is authenticated correctly."""
        auth = ApplicationPasswordAuth("admin", "testpassword")
        request = httpx.Request("GET", "https://example.com")
        
        authenticated = auth.authenticate(request)
        assert "Authorization" in authenticated.headers


class TestJWTAuth:
    """Tests for JWTAuth handler."""

    def test_init_without_token(self):
        """Test JWTAuth initialization without token."""
        auth = JWTAuth()
        assert auth.token is None

    def test_init_with_token(self):
        """Test JWTAuth initialization with token."""
        auth = JWTAuth(token="my_jwt_token")
        assert auth.token == "my_jwt_token"

    def test_get_headers_with_token(self):
        """Test that correct Authorization header is generated with token."""
        auth = JWTAuth(token="my_jwt_token")
        headers = auth.get_headers()
        assert headers == {"Authorization": "Bearer my_jwt_token"}

    def test_get_headers_without_token(self):
        """Test that empty headers returned without token."""
        auth = JWTAuth()
        headers = auth.get_headers()
        assert headers == {}

    def test_authenticate_request_with_token(self):
        """Test that request is authenticated correctly with token."""
        auth = JWTAuth(token="my_jwt_token")
        request = httpx.Request("GET", "https://example.com")
        
        authenticated = auth.authenticate(request)
        assert "Authorization" in authenticated.headers

    def test_authenticate_request_without_token(self):
        """Test that request passes through without token."""
        auth = JWTAuth()
        request = httpx.Request("GET", "https://example.com")
        
        authenticated = auth.authenticate(request)
        assert authenticated == request


class TestOAuth2Auth:
    """Tests for OAuth2Auth handler."""

    def test_init_without_tokens(self):
        """Test OAuth2Auth initialization without tokens."""
        auth = OAuth2Auth()
        assert auth.access_token is None
        assert auth.refresh_token is None

    def test_init_with_tokens(self):
        """Test OAuth2Auth initialization with tokens."""
        auth = OAuth2Auth(
            access_token="access123",
            refresh_token="refresh123",
            client_id="client123",
            client_secret="secret123",
        )
        assert auth.access_token == "access123"
        assert auth.refresh_token == "refresh123"
        assert auth.client_id == "client123"
        assert auth.client_secret == "secret123"

    def test_get_headers_with_token(self):
        """Test that correct Authorization header is generated."""
        auth = OAuth2Auth(access_token="access123")
        headers = auth.get_headers()
        assert headers == {"Authorization": "Bearer access123"}

    def test_get_headers_without_token(self):
        """Test that empty headers returned without token."""
        auth = OAuth2Auth()
        headers = auth.get_headers()
        assert headers == {}
