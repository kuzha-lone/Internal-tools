# TradeBrain Platform

A shared monorepo for the team. It combines two pipelines that already need to share one news layer:

1. **News engine** — scrapes free news sources and public Telegram channels, scores and categorizes each item (crypto / currency / economy), rewrites it in brand voice, and publishes to Telegram and the website. (This is the existing `implementation_plan_news_collector` plan, restructured to fit into this repo.)
2. **Trading engine** — a decision "brain" that takes the same categorized news as a fundamental bias filter, combines it with technical rules, and sends orders through MCP broker adapters (MT5, cTrader). TradingView is used as a signal/alert input only, not for execution — see `services/trading-engine/README.md` for why.
3. **Social distribution** — a separate worker that reads from the trade log and news log and posts daily recaps, decoupled from both pipelines so a posting bug can never touch a live order.
4. **Backtester / simulator** — a dependency-free paper-trading loop you can run today, before any broker credentials or real money exist.

Full system design: `ARCHITECTURE.md`. Build sequence: `docs/roadmap.md`. How to run your first simulation right now: `docs/simulation_guide.md`.

## Quickstart

```bash
git clone <this-repo-url>
cd tradebrain
cp .env.example .env            # fill in keys as each piece comes online — nothing required yet
pip install -r requirements.txt

# Runs immediately, no API keys or broker account needed:
python services/trading-engine/backtester/simulator.py
```

## Repository layout

```
tradebrain/
├── services/
│   ├── news-engine/          # collectors, MCP server, content brain -> telegram/website
│   ├── trading-engine/       # broker MCP adapters, decision brain, backtester, trade log
│   ├── social-distribution/  # scheduled recap poster (reads logs, never writes orders)
│   └── shared/               # db schema, config loader, logging used by every service
├── infra/                    # docker-compose, nginx
└── docs/                     # architecture, roadmap, simulation guide, compliance notes
```

## Ground rules for the team

- The trading brain never publishes to socials directly, and the social bot never has broker credentials. Keep that boundary even as the code grows.
- Nothing touches a live broker account until it has a logged track record from the simulator and then a demo account. See `docs/roadmap.md`.
- Each service has its own README with open questions — resolve those before extending that service, so we don't build on assumptions nobody agreed on.
