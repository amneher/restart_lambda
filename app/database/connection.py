import sqlite3
from contextlib import contextmanager
from typing import Generator
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "data.db")

_connection: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
    return _connection


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            retailer TEXT,
            affiliate_status TEXT,
            price REAL NOT NULL,
            quantity_needed INTEGER NOT NULL DEFAULT 1,
            quantity_purchased INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_items_timestamp
        AFTER UPDATE ON items
        BEGIN
            UPDATE items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    """)
    conn.commit()


def close_db() -> None:
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
