# News engine

Scrapes free news sources and public Telegram channels, dedupes and scores them, exposes them to both brains (content + trading) via one MCP server, and publishes curated content to Telegram and the website.

This is the original `implementation_plan_news_collector` plan, restructured to live inside the shared repo and to expose a tool the trading brain can also call.

## Layout
```
news-engine/
├── collector/
│   ├── main.py               # orchestrator, runs all scrapers on a schedule
│   ├── scrapers/
│   │   └── rss_scraper.py    # generic RSS/Atom parser, add others alongside it
│   └── queue/
│       └── store.py          # sqlite dedup store (sha256 of headline)
├── mcp_server/
│   └── server.py             # FastMCP: fetch / score / categorize / summarize
└── brain/
    └── agent.py               # content brain: picks top items, rewrites, publishes
```

## Open questions (carried over from the original plan, still unresolved)
- Which AI provider is primary for the content brain — Claude or Gemini?
- Posting frequency target: fully automated (~20-50/day) or curated (3-5/day)?
- Telegram private channel reading needs a real phone number for Telethon — available or public channels only for now?
- FinancialJuice's live WebSocket is browser-intended; scraping it may violate their ToS. Start with RSS/GDELT/public Telegram and revisit FinancialJuice separately if still wanted.
