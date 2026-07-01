"""
deduplicator.py — Tracks articles already sent to Telegram.
Prevents reposting the same story within the TTL window.
Uses a simple JSON file as persistent store.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory"
SEEN_FILE = MEMORY_DIR / "seen_stories.json"


def _load() -> dict:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not SEEN_FILE.exists():
        return {}
    try:
        with open(SEEN_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: dict):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _clean_expired(data: dict, ttl_hours: int) -> dict:
    """Remove entries older than TTL so the file doesn't grow forever."""
    now = datetime.now(timezone.utc)
    fresh = {}
    for story_id, meta in data.items():
        try:
            seen_at = datetime.fromisoformat(meta["seen_at"])
            age = (now - seen_at).total_seconds() / 3600
            if age <= ttl_hours:
                fresh[story_id] = meta
        except Exception:
            pass
    return fresh


def is_seen(story_id: str, ttl_hours: int = 24) -> bool:
    """Return True if this story was already posted within the TTL window."""
    data = _load()
    data = _clean_expired(data, ttl_hours)
    return story_id in data


def mark_seen(story_id: str, title: str = ""):
    """Record that this story has been posted."""
    data = _load()
    data[story_id] = {
        "title": title[:80],
        "seen_at": datetime.now(timezone.utc).isoformat(),
    }
    _save(data)


def filter_new(articles: list, ttl_hours: int = 24) -> list:
    """
    Filter a list of articles — returns only those not yet seen.
    Also cleans up expired entries as a side effect.
    """
    data = _load()
    data = _clean_expired(data, ttl_hours)
    _save(data)  # persist the cleaned version

    new_articles = []
    for art in articles:
        story_id = art.get("id", art.get("url", ""))
        if story_id and story_id not in data:
            new_articles.append(art)

    return new_articles


if __name__ == "__main__":
    # Quick test
    print("Seen file:", SEEN_FILE)
    test = {"id": "https://example.com/test", "title": "Test Article"}
    print("Is seen:", is_seen(test["id"]))
    mark_seen(test["id"], test["title"])
    print("After mark, is seen:", is_seen(test["id"]))
