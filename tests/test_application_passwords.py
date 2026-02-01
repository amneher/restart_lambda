"""Tests for Application Passwords endpoint."""

import pytest
import respx
import httpx

from wordpress_api import WordPressClient


class TestApplicationPasswordsEndpoint:
    """Tests for ApplicationPasswordsEndpoint."""

    @respx.mock
    def test_list_passwords(self, client, api_url, mock_application_password):
        """Test listing application passwords."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[mock_application_password])
        )
        
        passwords = client.application_passwords.list()
        assert len(passwords) == 1
        assert passwords[0].name == "Test App"

    @respx.mock
    def test_list_passwords_for_user(self, client, api_url, mock_application_password):
        """Test listing application passwords for specific user."""
        respx.get(f"{api_url}/wp/v2/users/1/application-passwords").mock(
            return_value=httpx.Response(200, json=[mock_application_password])
        )
        
        passwords = client.application_passwords.list(user_id=1)
        assert len(passwords) == 1

    @respx.mock
    def test_get_password(self, client, api_url, mock_application_password):
        """Test getting a specific application password."""
        uuid = mock_application_password["uuid"]
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords/{uuid}").mock(
            return_value=httpx.Response(200, json=mock_application_password)
        )
        
        password = client.application_passwords.get(uuid)
        assert password.uuid == uuid
        assert password.name == "Test App"

    @respx.mock
    def test_create_password(self, client, api_url, mock_application_password_created):
        """Test creating an application password."""
        respx.post(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(201, json=mock_application_password_created)
        )
        
        result = client.application_passwords.create("Test App")
        assert result.name == "Test App"
        assert result.password == "abcd efgh ijkl mnop"

    @respx.mock
    def test_update_password(self, client, api_url, mock_application_password):
        """Test updating an application password."""
        uuid = mock_application_password["uuid"]
        updated = {**mock_application_password, "name": "Renamed App"}
        respx.post(f"{api_url}/wp/v2/users/me/application-passwords/{uuid}").mock(
            return_value=httpx.Response(200, json=updated)
        )
        
        result = client.application_passwords.update(uuid, "Renamed App")
        assert result.name == "Renamed App"

    @respx.mock
    def test_delete_password(self, client, api_url, mock_application_password):
        """Test deleting an application password."""
        uuid = mock_application_password["uuid"]
        respx.delete(f"{api_url}/wp/v2/users/me/application-passwords/{uuid}").mock(
            return_value=httpx.Response(200, json={"deleted": True})
        )
        
        result = client.application_passwords.delete(uuid)
        assert result["deleted"] is True

    @respx.mock
    def test_delete_all_passwords(self, client, api_url):
        """Test deleting all application passwords."""
        respx.delete(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json={"deleted": 3})
        )
        
        result = client.application_passwords.delete_all()
        assert result["deleted"] == 3

    @respx.mock
    def test_get_or_create_existing(self, client, api_url, mock_application_password):
        """Test get_or_create returns existing password."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[mock_application_password])
        )
        
        result = client.application_passwords.get_or_create("Test App")
        assert result.name == "Test App"

    @respx.mock
    def test_get_or_create_new(self, client, api_url, mock_application_password_created):
        """Test get_or_create creates new password when none exists."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[])
        )
        respx.post(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(201, json=mock_application_password_created)
        )
        
        result = client.application_passwords.get_or_create("Test App")
        assert hasattr(result, "password")
        assert result.password == "abcd efgh ijkl mnop"

    @respx.mock
    def test_ensure_exists_returns_existing(self, client, api_url, mock_application_password):
        """Test ensure_exists returns existing with was_created=False."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[mock_application_password])
        )
        
        result, was_created = client.application_passwords.ensure_exists("Test App")
        assert result.name == "Test App"
        assert was_created is False

    @respx.mock
    def test_ensure_exists_creates_new(self, client, api_url, mock_application_password_created):
        """Test ensure_exists creates new with was_created=True."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[])
        )
        respx.post(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(201, json=mock_application_password_created)
        )
        
        result, was_created = client.application_passwords.ensure_exists("Test App")
        assert was_created is True
        assert result.password == "abcd efgh ijkl mnop"

    @respx.mock
    def test_has_any_true(self, client, api_url, mock_application_password):
        """Test has_any returns True when passwords exist."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[mock_application_password])
        )
        
        assert client.application_passwords.has_any() is True

    @respx.mock
    def test_has_any_false(self, client, api_url):
        """Test has_any returns False when no passwords exist."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[])
        )
        
        assert client.application_passwords.has_any() is False

    @respx.mock
    def test_count(self, client, api_url, mock_application_password):
        """Test count returns correct number."""
        respx.get(f"{api_url}/wp/v2/users/me/application-passwords").mock(
            return_value=httpx.Response(200, json=[
                mock_application_password,
                {**mock_application_password, "uuid": "different-uuid", "name": "Another App"},
            ])
        )
        
        assert client.application_passwords.count() == 2
