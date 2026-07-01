"""
News MCP server. Both the content brain and the trading brain call into this
-- it's the one place news scoring/categorization logic lives.
Run with: python mcp_server/server.py
"""
from fastmcp import FastMCP
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "collector"))
from queue.store import fetch_unprocessed, DB_PATH  # noqa: E402

mcp = FastMCP("news-engine")


@mcp.tool()
def fetch_latest_news(limit: int = 10, category: str = "all") -> list[dict]:
    """Fetch latest unprocessed news, optionally filtered by category
    (crypto | currency | economy)."""
    cat = None if category == "all" else category
    return fetch_unprocessed(limit=limit, category=cat, path=DB_PATH)


@mcp.tool()
def score_narrative(headline: str, body: str = "", source: str = "") -> dict:
    """Score a news item for sentiment (-1..1) and impact/urgency (0-100).
    TODO: replace this keyword heuristic with a FinBERT-style classifier
    once volume justifies it -- see ARCHITECTURE.md."""
    positive_words = {"surge", "rally", "growth", "beat", "rises", "gain"}
    negative_words = {"crash", "plunge", "recession", "miss", "falls", "drop"}
    text = (headline + " " + body).lower()
    score = sum(w in text for w in positive_words) - sum(w in text for w in negative_words)
    sentiment = max(-1.0, min(1.0, score / 3))
    impact = 50 + abs(score) * 15
    return {"sentiment_score": sentiment, "impact_score": min(100, impact)}


@mcp.tool()
def tag_category(headline: str, body: str = "") -> str:
    """Classify into crypto | currency | economy | other."""
    text = (headline + " " + body).lower()
    if any(w in text for w in ["bitcoin", "crypto", "ethereum", "btc", "eth"]):
        return "crypto"
    if any(w in text for w in ["dollar", "euro", "yen", "forex", "currency", "exchange rate"]):
        return "currency"
    if any(w in text for w in ["gdp", "inflation", "fed", "rate hike", "jobs report", "cpi"]):
        return "economy"
    return "other"


@mcp.tool()
def summarize_news(headline: str, body: str, style: str = "telegram") -> str:
    """Rewrite news in brand voice. TODO: call the Anthropic API here with
    the SYSTEM.md brand voice rules -- this is a placeholder passthrough."""
    return f"{headline}\n\n{body[:280]}"


if __name__ == "__main__":
    mcp.run()
