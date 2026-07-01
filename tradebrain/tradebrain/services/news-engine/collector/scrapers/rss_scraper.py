"""Generic RSS/Atom scraper. Add a new feed by adding an entry to sources.json,
not by writing a new file -- this one handles any standard feed."""
import hashlib
import feedparser


def fetch_feed(name: str, url: str, category: str) -> list[dict]:
    parsed = feedparser.parse(url)
    items = []
    for entry in parsed.entries:
        headline = entry.get("title", "").strip()
        if not headline:
            continue
        item_id = hashlib.sha256(headline.lower().encode()).hexdigest()
        items.append({
            "id": item_id,
            "source": name,
            "headline": headline,
            "body": entry.get("summary", ""),
            "category": category,
            "published_at": entry.get("published", ""),
        })
    return items
