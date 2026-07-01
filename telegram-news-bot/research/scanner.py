"""
scanner.py — Fetches news articles from RSS feeds and optional APIs.
Returns a list of standardized article dicts.
"""

import json
import os
import time
import feedparser
import requests
from datetime import datetime, timezone
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_sources() -> list:
    with open(CONFIG_DIR / "sources.json") as f:
        return json.load(f)


def load_settings() -> dict:
    with open(CONFIG_DIR / "settings.json") as f:
        return json.load(f)


def parse_feed_time(entry) -> datetime:
    """Try to extract a published datetime from an RSS entry."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def fetch_rss(source: dict, max_age_hours: int) -> list:
    """Fetch and filter one RSS feed source."""
    articles = []
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (compatible; TelegramNewsBot/1.0)"
            )
        }
        # feedparser can take a url directly
        feed = feedparser.parse(source["url"], request_headers=headers)
        now = datetime.now(timezone.utc)

        for entry in feed.entries:
            pub = parse_feed_time(entry)
            age_hours = (now - pub).total_seconds() / 3600

            if age_hours > max_age_hours:
                continue  # too old

            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            summary = getattr(entry, "summary", "").strip()

            # Clean HTML tags from summary
            import re
            summary = re.sub(r"<[^>]+>", "", summary)
            summary = summary[:300].strip()

            if not title or not link:
                continue

            articles.append({
                "id": link,                    # use link as unique ID
                "title": title,
                "summary": summary,
                "url": link,
                "source": source["name"],
                "category": source.get("category", "general"),
                "published_at": pub.isoformat(),
                "age_hours": round(age_hours, 2),
            })

    except Exception as e:
        print(f"[scanner] Error fetching {source['name']}: {e}")

    return articles


def fetch_gnews(api_key: str, keywords: list, max_age_hours: int) -> list:
    """Fetch from GNews API if key is configured."""
    articles = []
    if not api_key:
        return articles
    try:
        query = " OR ".join(keywords[:5])
        url = (
            f"https://gnews.io/api/v4/search"
            f"?q={requests.utils.quote(query)}"
            f"&lang=en&max=10&token={api_key}"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        now = datetime.now(timezone.utc)

        for item in data.get("articles", []):
            pub_str = item.get("publishedAt", "")
            try:
                pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
            except Exception:
                pub = now

            age_hours = (now - pub).total_seconds() / 3600
            if age_hours > max_age_hours:
                continue

            articles.append({
                "id": item.get("url", ""),
                "title": item.get("title", "").strip(),
                "summary": item.get("description", "").strip()[:300],
                "url": item.get("url", ""),
                "source": item.get("source", {}).get("name", "GNews"),
                "category": "general",
                "published_at": pub.isoformat(),
                "age_hours": round(age_hours, 2),
            })
    except Exception as e:
        print(f"[scanner] GNews error: {e}")

    return articles


def fetch_all() -> list:
    """
    Main entry point. Scans all configured sources and returns
    a deduplicated, merged list of articles.
    """
    settings = load_settings()
    sources = load_sources()
    max_age = settings.get("story_age_hours", 6)
    keywords = settings.get("keywords", [])

    all_articles = []
    seen_ids = set()

    # RSS feeds
    for source in sources:
        results = fetch_rss(source, max_age_hours=max_age)
        for art in results:
            if art["id"] not in seen_ids:
                seen_ids.add(art["id"])
                all_articles.append(art)
        # Small polite delay between feeds
        time.sleep(0.5)

    # GNews API (optional)
    gnews_key = os.getenv("GNEWS_API_KEY", "")
    if gnews_key:
        gnews_results = fetch_gnews(gnews_key, keywords, max_age)
        for art in gnews_results:
            if art["id"] not in seen_ids:
                seen_ids.add(art["id"])
                all_articles.append(art)

    # Sort: newest first
    all_articles.sort(key=lambda x: x.get("age_hours", 99))

    print(f"[scanner] Found {len(all_articles)} articles across all sources")
    return all_articles


if __name__ == "__main__":
    # Quick test run
    articles = fetch_all()
    for a in articles[:5]:
        print(f"\n[{a['source']}] {a['title']}")
        print(f"  Age: {a['age_hours']}h | {a['url']}")
