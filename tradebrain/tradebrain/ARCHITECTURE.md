# Architecture

## Why one news layer feeds two brains

The news engine and the trading engine both need the same scraped, scored, categorized news. Rather than building two scrapers, one collector and one MCP server serve both a "content brain" (rewrites news for Telegram/website) and a "trading brain" (uses the same category + sentiment score as a fundamental bias filter). This is the only point where the two pipelines touch.

```
                         ┌──────────────────────────────┐
                         │         SOURCE LAYER          │
                         │ RSS feeds, free news APIs,    │
                         │ public Telegram channels,     │
                         │ GDELT                         │
                         └───────────────┬────────────────┘
                                         │ poll every 1-5 min
                                         ▼
                         ┌──────────────────────────────┐
                         │      COLLECTOR SERVICE        │
                         │ dedup (sha256) · normalize ·  │
                         │ priority score                │
                         └───────────────┬────────────────┘
                                         ▼
                         ┌──────────────────────────────┐
                         │   NEWS MCP SERVER (FastMCP)   │
                         │ fetch_latest_news()           │
                         │ score_narrative()             │
                         │ tag_category()  crypto/fx/macro│
                         │ summarize_news()              │
                         └───────────────┬────────────────┘
                       ┌─────────────────┴──────────────────┐
                       ▼                                     ▼
        ┌───────────────────────────┐         ┌───────────────────────────┐
        │       CONTENT BRAIN        │         │       TRADING BRAIN        │
        │ rewrites in brand voice    │         │ news bias + technical      │
        │ from SYSTEM.md             │         │ rules -> trade signal      │
        └─────────────┬───────────────┘         └─────────────┬───────────────┘
                      ▼                                       ▼
        ┌───────────────────────────┐         ┌───────────────────────────┐
        │  TELEGRAM CHANNEL +        │         │   TRADING MCP SERVER       │
        │  WEBSITE (Next.js)         │         │  MT5 adapter / cTrader     │
        └─────────────┬───────────────┘         │  adapter (TradingView is  │
                      │                          │  signal-only, see below)  │
                      │                          └─────────────┬───────────────┘
                      │                                        ▼
                      │                          ┌───────────────────────────┐
                      │                          │     TRADE LOG (outcomes)   │
                      │                          │ feeds weekly retraining of │
                      │                          │ the trading brain          │
                      │                          └─────────────┬───────────────┘
                      └───────────────────┬────────────────────┘
                                          ▼
                         ┌──────────────────────────────┐
                         │   SOCIAL DISTRIBUTION WORKER  │
                         │ reads trade_log + news_log,   │
                         │ posts daily recap. No broker  │
                         │ credentials, no order access. │
                         └──────────────────────────────┘
```

## Component notes

**Collector service.** Python, APScheduler, SQLite or Redis queue for the MVP — see `services/news-engine/README.md`. FinancialJuice's live WebSocket is flagged in the original plan as a ToS risk; RSS, GDELT, and public Telegram channels are the safe starting sources.

**News MCP server.** FastMCP, stdio locally / HTTP+SSE once deployed. Exposes the same tools to both brains so neither one re-implements scoring logic.

**Trading brain.** Not a live-updating RL agent — that's a much harder and less stable thing to get right than it sounds. It's a scoring model (start rule-based, evolve to gradient-boosted) that takes the news bias as a filter and combines it with technical signals. Every decision is logged with its full feature vector so the weekly retraining step has something to learn from. See `services/trading-engine/brain/decision_engine.py`.

**Trading MCP server(s).** One MCP server per broker, all exposing the same tool interface (`place_order`, `get_positions`, `close_position`, `get_account_state`) so the brain doesn't care which broker it's talking to. Two platform notes that affect server planning directly:
- MT5's official Python package only talks to a running MT5 terminal, and that terminal only runs natively on Windows (Wine works but adds operational fragility). If the team is deploying on Linux VPS/containers for everything else, the MT5 adapter likely needs its own small Windows VPS or a Windows container, while everything else stays on Linux.
- cTrader's Open API is a proper OAuth-based REST/FIX-style API and runs anywhere, including the same Linux box as the rest of the stack — it's the easier one to containerize.
- TradingView has no public order-execution API for arbitrary accounts; treat its alerts/webhooks purely as an additional technical signal into the brain, not an execution path.

**Trade log.** SQLite for local dev and the simulator, Postgres (`services/shared/db/schema.sql`) once this is shared infrastructure. This table is the only thing the retraining step and the social bot both read from.

**Social distribution worker.** Deliberately has no access to broker credentials or the trading MCP server — it only reads `trade_log` and `news_items`. This is the boundary that keeps a posting bug from ever becoming a trading bug.

## Server / deployment shape

For the team's first shared environment, a single Linux VPS (Hetzner/DigitalOcean, 2-4 vCPU is plenty at this stage) running everything via `docker-compose` except the MT5 adapter, which needs Windows — keep that as a separate small Windows VM or VPS that exposes its MCP server over the network to the rest of the stack. Postgres and Redis can run as containers on the same Linux box initially; move to managed services (Supabase, Upstash) once more than one person needs reliable access to the data. See `infra/` for the compose file and `docs/roadmap.md` for when to introduce each piece.
