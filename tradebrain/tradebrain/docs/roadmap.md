# Build roadmap

This sequences the news engine (already scoped in the original implementation plan) and the trading engine together, since they share the news layer.

## Phase 0 — Foundation (week 1)
- [ ] Repo + env setup, shared Postgres/SQLite schema agreed (`services/shared/db/schema.sql`)
- [ ] RSS + public Telegram scrapers running, deduped, stored
- [ ] Run `python services/trading-engine/backtester/simulator.py` — confirms the trading loop's shape end-to-end on synthetic data before any real source is wired in

## Phase 1 — News MCP + content brain (week 2-3)
- [ ] FastMCP server with fetch / score / categorize / summarize tools
- [ ] Content brain wired to Telegram + website publish tools
- [ ] Full pipeline test: scraped item -> Telegram message out

## Phase 2 — Trading brain on paper, forex only (week 3-5)
- [ ] MT5 demo account, MT5 MCP adapter built and tested against it
- [ ] Decision engine combines real news bias (from the same MCP server as Phase 1) with technical rules
- [ ] Every trade logged with its full feature vector to `trade_log`
- [ ] Target: 100-200+ logged demo trades before judging anything — this is the minimum for the weekly retraining step to mean anything statistically

## Phase 3 — Retraining loop + social distribution (week 5-6)
- [ ] Weekly retraining job reads `trade_log`, refits the scoring model, compares against the previous version before swapping it in (never auto-promote a new model without this comparison)
- [ ] Social distribution worker posts daily recap from `trade_log` + `news_items` — kept on its own credentials, no broker access
- [ ] Add cTrader as a second broker adapter for redundancy and to diversify away from MT5-only risk

## Phase 4 — Expand instruments, still on paper (week 6-8)
- [ ] Add indices/CFDs in the same demo environment
- [ ] Only now evaluate the Indian market specifically as its own compliance project — SEBI's 2025/2026 retail algo rules require strategies to be registered and routed through the broker with an exchange-issued strategy ID once you're not just a casual API user (the practical threshold is 10 orders/second; below that you're a regular API user). Budget this as its own phase with a broker that supports it (e.g. Kite Connect, Upstox), not a bolt-on to the existing forex stack.

## Phase 5 — Live, smallest size first
- [ ] Go live only after a demo track record spanning more than one market regime, not just a lucky two weeks
- [ ] Confirm the specific broker's terms of service permit automated/API trading on that account type
- [ ] Start at the smallest position size the broker allows, scale gradually based on logged live performance, not demo performance — the two are not the same thing once slippage, latency, and real psychology enter the picture
