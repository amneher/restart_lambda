import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_PATH"] = ":memory:"

from app.main import app
from app.database import init_db, close_db, get_connection


@pytest.fixture(scope="function")
def client():
    init_db()
    with TestClient(app) as test_client:
        yield test_client
    close_db()


@pytest.fixture(scope="function")
def db_connection():
    init_db()
    conn = get_connection()
    yield conn
    close_db()


@pytest.fixture
def sample_item():
    return {
        "name": "Test Item",
        "description": "A test item description",
        "price": 29.99,
        "is_active": True
    }


@pytest.fixture
def sample_items():
    return [
        {"name": "Item 1", "description": "First item", "price": 10.00, "is_active": True},
        {"name": "Item 2", "description": "Second item", "price": 20.00, "is_active": True},
        {"name": "Item 3", "description": "Third item", "price": 30.00, "is_active": False},
    ]
