import os
import pytest

os.environ["DATABASE_PATH"] = ":memory:"

from app.database import init_db, close_db, get_db, get_connection


class TestDatabase:
    def test_init_db_creates_table(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='items'"
        )
        result = cursor.fetchone()
        assert result is not None
        assert result["name"] == "items"

    def test_init_db_creates_trigger(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' AND name='update_items_timestamp'"
        )
        result = cursor.fetchone()
        assert result is not None

    def test_get_db_context_manager(self, db_connection):
        with get_db() as conn:
            assert conn is not None
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1

    def test_insert_and_retrieve(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, url, price) VALUES (?, ?, ?)",
            ("Test Item", "https://example.com/product/test", 25.00)
        )
        db_connection.commit()
        
        cursor.execute("SELECT * FROM items WHERE name = ?", ("Test Item",))
        row = cursor.fetchone()
        assert row is not None
        assert row["name"] == "Test Item"
        assert row["price"] == 25.00

    def test_update_timestamp_trigger(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, url, price) VALUES (?, ?, ?)",
            ("Trigger Test", "https://example.com/product/trigger-test", 10.00)
        )
        db_connection.commit()
        
        cursor.execute("SELECT created_at, updated_at FROM items WHERE name = ?", ("Trigger Test",))
        row = cursor.fetchone()
        original_updated = row["updated_at"]
        
        import time
        time.sleep(0.1)
        
        cursor.execute("UPDATE items SET price = ? WHERE name = ?", (20.00, "Trigger Test"))
        db_connection.commit()
        
        cursor.execute("SELECT updated_at FROM items WHERE name = ?", ("Trigger Test",))
        row = cursor.fetchone()
        new_updated = row["updated_at"]
        
        assert new_updated >= original_updated
