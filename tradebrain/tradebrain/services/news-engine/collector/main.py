"""Orchestrator: polls every configured source on its own interval and
writes new items into the dedup store. Run with: python collector/main.py"""
import json
import time
from pathlib import Path

from scrapers.rss_scraper import fetch_feed
from queue.store import init_db, insert_if_new

SOURCES_PATH = Path(__file__).parent / "config" / "sources.json"

DEFAULT_SOURCES = {
    "rss_feeds": [
        {"name": "Google News - Finance",
         "url": "https://news.google.com/rss/search?q=finance+markets&hl=en&gl=US&ceid=US:en",
         "category": "economy", "poll_interval_seconds": 120},
        {"name": "CoinTelegraph",
         "url": "https://cointelegraph.com/rss",
         "category": "crypto", "poll_interval_seconds": 180},
    ]
}


def load_sources() -> dict:
    if SOURCES_PATH.exists():
        return json.loads(SOURCES_PATH.read_text())
    return DEFAULT_SOURCES


def run_once(sources: dict) -> int:
    new_count = 0
    for feed in sources.get("rss_feeds", []):
        try:
            items = fetch_feed(feed["name"], feed["url"], feed["category"])
        except Exception as e:
            print(f"[collector] {feed['name']} failed: {e}")
            continue
        for item in items:
            if insert_if_new(item):
                new_count += 1
    return new_count


if __name__ == "__main__":
    init_db()
    sources = load_sources()
    print(f"[collector] loaded {len(sources.get('rss_feeds', []))} RSS sources. Polling every 120s, Ctrl+C to stop.")
    while True:
        n = run_once(sources)
        print(f"[collector] cycle complete, {n} new items")
        time.sleep(120)
