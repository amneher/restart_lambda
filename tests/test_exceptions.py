"""Tests for exception classes."""

import pytest

from wordpress_api.exceptions import (
    WordPressError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    PermissionError,
    raise_for_status,
)


class TestWordPressError:
    """Tests for WordPressError base class."""

    def test_init_basic(self):
        """Test basic initialization."""
        error = WordPressError("Something went wrong")
        assert error.message == "Something went wrong"
        assert error.status_code is None
        assert error.error_code is None
        assert error.data == {}

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        error = WordPressError(
            "Error message",
            status_code=400,
            error_code="invalid_param",
            data={"field": "title"},
        )
        assert error.message == "Error message"
        assert error.status_code == 400
        assert error.error_code == "invalid_param"
        assert error.data == {"field": "title"}

    def test_str_representation(self):
        """Test string representation."""
        error = WordPressError("Error", status_code=400, error_code="bad_request")
        result = str(error)
        assert "Error" in result
        assert "400" in result
        assert "bad_request" in result


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_is_wordpress_error(self):
        """Test that AuthenticationError is a WordPressError."""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, WordPressError)


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_is_wordpress_error(self):
        """Test that NotFoundError is a WordPressError."""
        error = NotFoundError("Resource not found")
        assert isinstance(error, WordPressError)


class TestValidationError:
    """Tests for ValidationError."""

    def test_is_wordpress_error(self):
        """Test that ValidationError is a WordPressError."""
        error = ValidationError("Invalid data")
        assert isinstance(error, WordPressError)


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_is_wordpress_error(self):
        """Test that RateLimitError is a WordPressError."""
        error = RateLimitError("Rate limit exceeded")
        assert isinstance(error, WordPressError)


class TestServerError:
    """Tests for ServerError."""

    def test_is_wordpress_error(self):
        """Test that ServerError is a WordPressError."""
        error = ServerError("Internal server error")
        assert isinstance(error, WordPressError)


class TestRaiseForStatus:
    """Tests for raise_for_status function."""

    def test_401_raises_authentication_error(self):
        """Test that 401 raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            raise_for_status(401, {"message": "Invalid credentials"})

    def test_403_raises_permission_error(self):
        """Test that 403 raises PermissionError."""
        with pytest.raises(PermissionError):
            raise_for_status(403, {"message": "Forbidden"})

    def test_404_raises_not_found_error(self):
        """Test that 404 raises NotFoundError."""
        with pytest.raises(NotFoundError):
            raise_for_status(404, {"message": "Not found"})

    def test_400_raises_validation_error(self):
        """Test that 400 raises ValidationError."""
        with pytest.raises(ValidationError):
            raise_for_status(400, {"message": "Invalid data"})

    def test_429_raises_rate_limit_error(self):
        """Test that 429 raises RateLimitError."""
        with pytest.raises(RateLimitError):
            raise_for_status(429, {"message": "Rate limited"})

    def test_500_raises_server_error(self):
        """Test that 500 raises ServerError."""
        with pytest.raises(ServerError):
            raise_for_status(500, {"message": "Internal error"})

    def test_503_raises_server_error(self):
        """Test that 503 raises ServerError."""
        with pytest.raises(ServerError):
            raise_for_status(503, {"message": "Service unavailable"})

    def test_other_4xx_raises_wordpress_error(self):
        """Test that other 4xx codes raise WordPressError."""
        with pytest.raises(WordPressError):
            raise_for_status(418, {"message": "I'm a teapot"})

    def test_2xx_does_not_raise(self):
        """Test that 2xx status codes don't raise."""
        raise_for_status(200, {})
        raise_for_status(201, {})
        raise_for_status(204, {})
