"""SQLite-backed dedup store for local dev. Swap for the Postgres
news_items table (services/shared/db/schema.sql) once this is shared infra."""
import sqlite3
from contextlib import closing

DB_PATH = "news_queue.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS news_items (
    id TEXT PRIMARY KEY,
    source TEXT,
    headline TEXT,
    body TEXT,
    category TEXT,
    sentiment_score REAL,
    impact_score INTEGER,
    published_at TEXT,
    processed INTEGER DEFAULT 0
);
"""


def init_db(path: str = DB_PATH) -> None:
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(SCHEMA)
        conn.commit()


def insert_if_new(item: dict, path: str = DB_PATH) -> bool:
    """Returns True if the item was new (inserted), False if it was a duplicate."""
    with closing(sqlite3.connect(path)) as conn:
        cur = conn.execute("SELECT 1 FROM news_items WHERE id = ?", (item["id"],))
        if cur.fetchone():
            return False
        conn.execute(
            "INSERT INTO news_items (id, source, headline, body, category, published_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (item["id"], item["source"], item["headline"], item.get("body", ""),
             item.get("category", ""), item.get("published_at", "")),
        )
        conn.commit()
        return True


def fetch_unprocessed(limit: int = 10, category: str | None = None, path: str = DB_PATH) -> list[dict]:
    with closing(sqlite3.connect(path)) as conn:
        conn.row_factory = sqlite3.Row
        if category:
            rows = conn.execute(
                "SELECT * FROM news_items WHERE processed = 0 AND category = ? "
                "ORDER BY published_at DESC LIMIT ?", (category, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM news_items WHERE processed = 0 "
                "ORDER BY published_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]
