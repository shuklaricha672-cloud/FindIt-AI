import sqlite3
from datetime import datetime

DB_NAME = "findit.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL,
            description TEXT,
            location TEXT,
            status TEXT NOT NULL,
            image_path TEXT,
            contact TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_item(
    item_type,
    description,
    location,
    status,
    image_path,
    contact
):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items
        (
            item_type,
            description,
            location,
            status,
            image_path,
            contact,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        item_type,
        description,
        location,
        status,
        image_path,
        contact,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_items(status=None):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    if status:
        cursor.execute("""
            SELECT *
            FROM items
            WHERE status = ?
            ORDER BY id DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT *
            FROM items
            ORDER BY id DESC
        """)

    items = cursor.fetchall()

    conn.close()

    return items