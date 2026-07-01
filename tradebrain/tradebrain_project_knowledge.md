# TradeBrain + News Character — Full Project Knowledge

> **Last updated:** June 2026  
> **Scope:** End-to-end reference for the news-character pipeline, the trading brain, and how the two fit together in the shared `tradebrain` monorepo.

---

## Table of Contents

1. [What This System Is](#1-what-this-system-is)
2. [Where the Code Lives](#2-where-the-code-lives)
3. [Full Architecture](#3-full-architecture)
4. [Plan Assessment — What Is Correct](#4-plan-assessment--what-is-correct)
5. [Plan Assessment — Mistakes & Missing Points](#5-plan-assessment--mistakes--missing-points)
6. [APIs, Subscriptions & Credentials Needed](#6-apis-subscriptions--credentials-needed)
7. [Cost Breakdown](#7-cost-breakdown)
8. [Where Data Lives](#8-where-data-lives)
9. [Deployment Options](#9-deployment-options)
10. [Open Decisions (Unresolved)](#10-open-decisions-unresolved)
11. [Build Sequence Summary](#11-build-sequence-summary)

---

## 1. What This System Is

Two interconnected pipelines that share one news layer:

| Pipeline | Purpose |
|---|---|
| **News Character** | Scrapes real-time news → AI brain rewrites in brand voice → publishes to Telegram channel + website → triggers 3×/day short-form video workflow |
| **Trading Brain** | Uses the same scored news as a fundamental bias filter → combines with technical rules → sends orders to MT5 / cTrader broker adapters |
| **Social Distribution** | Reads trade log + news log → posts daily recaps. Deliberately isolated: no broker credentials, no order access |

The **key design insight**: one shared collector + one shared MCP news server feeds both brains. Neither pipeline rebuilds the scraper independently. This is correct and efficient.

---

## 2. Where the Code Lives

### Monorepo Root
```
C:\Beew\savage\tradebrain\tradebrain\
```

### Full Directory Map
```
tradebrain/
├── .env.example                        ← all secrets template (never commit real .env)
├── .gitignore
├── requirements.txt                    ← Python dependencies for all services
├── ARCHITECTURE.md                     ← system design doc (canonical reference)
├── README.md                           ← quickstart + repo layout
│
├── services/
│   ├── news-engine/                    ← Phase 1 news character pipeline
│   │   ├── collector/
│   │   │   ├── main.py                 ← orchestrator, runs all scrapers on APScheduler
│   │   │   ├── scrapers/
│   │   │   │   └── rss_scraper.py      ← generic RSS/Atom parser (add others alongside)
│   │   │   └── queue/
│   │   │       └── store.py            ← SQLite dedup store (SHA-256 of headline)
│   │   ├── mcp_server/
│   │   │   └── server.py               ← FastMCP: fetch/score/categorize/summarize tools
│   │   └── brain/
│   │       └── agent.py                ← content brain: picks top items, rewrites, publishes
│   │
│   ├── trading-engine/                 ← Phase 2+ trading pipeline
│   │   ├── mcp_server/
│   │   │   ├── mt5_server.py           ← MT5 adapter (Windows only — see deployment note)
│   │   │   └── ctrader_server.py       ← cTrader adapter (runs anywhere)
│   │   ├── brain/
│   │   │   ├── decision_engine.py      ← news bias + technical rules → trade signal
│   │   │   └── train.py                ← weekly retraining job (reads trade_log)
│   │   ├── backtester/
│   │   │   └── simulator.py            ← stdlib-only paper trading loop (run today, no API needed)
│   │   └── trade_log/
│   │       └── schema.sql              ← local SQLite mirror of shared schema
│   │
│   ├── social-distribution/            ← Phase 3 recap posting
│   │   ├── scheduler.py
│   │   └── telegram_bot.py
│   │
│   └── shared/
│       ├── config/                     ← shared config loader
│       ├── db/                         ← Postgres schema (shared/db/schema.sql)
│       └── utils/                      ← logging, helpers used by all services
│
├── infra/
│   ├── docker-compose.yml              ← Linux-host stack (MT5 intentionally excluded)
│   └── nginx/
│
└── docs/
    ├── roadmap.md                      ← phased build sequence
    ├── simulation_guide.md             ← 3-stage path to live trading
    └── (compliance notes — TBD)
```

### News Character Skill (Separate Repo)
```
C:\Beew\savage\trending-news-character-skill-v3\
├── implementation_plan_news_collector  ← original design doc (now absorbed into tradebrain)
└── trending-news-character-skill-sanitized\
    ├── START_HERE.md                   ← human setup guide
    ├── SYSTEM.md                       ← character brand voice + video rules
    ├── AGENTS.md                       ← agent context and rules
    ├── AGENT_RUNBOOK.md                ← step-by-step agent execution guide
    ├── config/                         ← project.json, research.json, video.json
    ├── brand/
    ├── skills/
    ├── workflows/
    ├── platforms/
    ├── memory/
    ├── output/
    └── scripts/
```

> [!IMPORTANT]
> The `implementation_plan_news_collector` file in v3 is the **original design** — it has now been restructured and lives inside the `tradebrain` monorepo as `services/news-engine/`. The v3 skill folder contains the **video character workflow** (HeyGen + HyperFrames + FFmpeg pipeline). These are two distinct things that connect at one point: the news brain triggers the video workflow 3×/day.

---

## 3. Full Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         SOURCE LAYER                              │
│  RSS feeds (Reuters, Google News, Yahoo, Bloomberg, CoinTelegraph)│
│  GDELT Project API  │  Public Telegram channels (httpx scrape)    │
│  [Optional later: FinancialJuice WS — ToS risk, see §5]          │
└──────────────────────────────┬───────────────────────────────────┘
                               │ poll every 60–300 sec per source
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                     COLLECTOR SERVICE (Python)                    │
│  APScheduler  │  SHA-256 dedup  │  Normalize  │  Priority score  │
│  Queue: SQLite (dev) → Postgres (prod)                           │
└──────────────────────────────┬───────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                  NEWS MCP SERVER (FastMCP)                        │
│  fetch_latest_news()   score_narrative()   tag_category()        │
│  summarize_news()      mark_processed()    get_queue_status()    │
│                                                                  │
│  ← SHARED: both Content Brain and Trading Brain call this        │
└───────────────────┬──────────────────────────┬───────────────────┘
                    │                          │
          ┌─────────▼──────────┐    ┌──────────▼──────────┐
          │   CONTENT BRAIN    │    │   TRADING BRAIN      │
          │ (news-engine/      │    │ (trading-engine/     │
          │  brain/agent.py)   │    │  brain/decision_     │
          │                    │    │  engine.py)          │
          │ Picks top 1–3 items│    │ news bias + tech      │
          │ Rewrites brand voice│   │ rules → trade signal  │
          │ Publishes:         │    └──────────┬───────────┘
          │  • Telegram channel│               │
          │  • Website API     │    ┌──────────▼───────────┐
          │ Triggers 3×/day    │    │  TRADING MCP SERVERS  │
          │  video workflow    │    │  mt5_server.py (Win)  │
          └─────────┬──────────┘    │  ctrader_server.py   │
                    │               └──────────┬───────────┘
          ┌─────────▼──────────┐               │
          │  PUBLISH LAYER     │    ┌──────────▼───────────┐
          │ Telegram Bot       │    │    TRADE LOG (DB)     │
          │ Website (Next.js)  │    │  logs every decision  │
          │ 3×/day video       │    │  + full feature vector│
          │  (HeyGen +         │    └──────────┬───────────┘
          │   HyperFrames +    │               │
          │   FFmpeg)          │    ┌──────────▼───────────┐
          └─────────┬──────────┘    │ WEEKLY RETRAINING     │
                    │               │ train.py reads log,   │
                    └───────────────┤ refits scoring model  │
                                    └──────────┬───────────┘
                                               │
                                    ┌──────────▼───────────┐
                                    │ SOCIAL DISTRIBUTION   │
                                    │ reads trade_log +     │
                                    │ news_log → daily recap│
                                    │ NO broker credentials │
                                    └───────────────────────┘
```

### The One Connection Point
The **news brain** calls `score_narrative()` on the MCP server → result flows to both the content pipeline (for editorial judgment) and the trading pipeline (as a bias score input to the decision engine). **Neither pipeline ever re-scrapes or re-scores independently.**

---

## 4. Plan Assessment — What Is Correct

The `implementation_plan_news_collector` plan (v3) is **architecturally sound**. Here is what it gets right:

| ✅ Correct Design Decision | Why It Matters |
|---|---|
| **Single collector + shared MCP server** | Avoids duplicate scraping. Both brains get identical scored data. |
| **SHA-256 deduplication** on headline text | Prevents the same story from being processed and posted multiple times |
| **FastMCP for the MCP server** | Correct framework choice — lightweight, Pythonic, well-suited for this |
| **SQLite first, Redis/Postgres later** | Right MVP path. Start simple, scale storage when you need to |
| **APScheduler for polling** | Good fit for a Python scheduler without a heavy dependency like Celery |
| **Telethon for Telegram reading** | Correct library for MTProto access. Public channel scraping via httpx is the right fallback |
| **python-telegram-bot v20+ (async)** | Correct modern choice for the bot publisher |
| **Next.js for the website** | Good choice — SSR + Supabase Realtime for live feed works well |
| **Vercel for website hosting** | Free, zero-ops, correct for a Next.js frontend |
| **Supabase for DB + Realtime** | Good choice — free tier, Postgres, built-in realtime broadcast for live feed |
| **Score-gated posting** | Breaking alert only at score >90, standard at 70–90 — sensible threshold design |
| **FinancialJuice ToS warning included** | Flagging this is the right call — their WebSocket is browser-intended |
| **5-week phased rollout** | Realistic and correctly sequenced (collector first, then MCP, then brain, then website) |
| **Brand voice rules in SYSTEM.md** | Correct — centralizing voice rules means the AI brain, video workflow, and Telegram bot all draw from the same source |

---

## 5. Plan Assessment — Mistakes & Missing Points

> [!CAUTION]
> These are gaps that will cause real problems if not addressed before or during build.

### 🔴 Critical Gaps

#### 1. The video workflow is not wired into the plan
The `implementation_plan_news_collector` describes the news pipeline well but **never connects it to the video character skill** (HeyGen + HyperFrames + FFmpeg). The plan says "3×/day trigger full character video workflow" as one bullet point — but this is the most complex piece of the whole system and needs its own sub-plan.

**What is missing:**
- How does `agent.py` trigger the video workflow? (subprocess call? API? direct agent invocation?)
- Does the video workflow read from the news MCP server, or does the agent pass the selected story in as a parameter?
- How is the `trending-news-character-skill-sanitized/` folder integrated — does it run as a separate agent process?
- Where do rendered videos go and how are they posted?

#### 2. No error handling / alerting plan
The plan mentions error alerting ("Telegram DM to self on failures") in Week 5 as a polish step. This should be **Week 1 infrastructure**. If the collector crashes silently at 3 AM, you won't know for hours. You need a dead-man's switch from day one.

**Fix:** Add a `ALERT_TELEGRAM_USER_ID` env var and a simple watchdog that DMs you if any service hasn't reported a heartbeat in N minutes.

#### 3. No rate limiting / backoff on scrapers
The plan has no mention of exponential backoff, retry logic, or rate limiting for scrapers. RSS feeds and APIs will occasionally return 429 or 503. Without this, the collector will crash or get IP-banned.

**Fix:** Wrap all HTTP calls in `httpx` with retry middleware (`tenacity` library or `httpx-retry`). Add `Retry-After` header parsing.

#### 4. The `summarize_news` MCP tool is doing AI work on the MCP server — wrong layer
The plan has `summarize_news()` as an MCP tool that rewrites in brand voice. But the **AI call should happen in `agent.py` (the brain layer)**, not inside the MCP server. The MCP server should be a dumb data/action layer, not where LLM inference happens. Mixing them makes the server stateful and expensive to run.

**Fix:** `summarize_news()` MCP tool should accept a raw item and return it unchanged, or be removed. The brain (`agent.py`) should call the AI API directly to do the rewrite, then call `publish_to_telegram()` with the result.

#### 5. No content deduplication on the publish side
SHA-256 dedup on ingest is good, but what happens if `agent.py` crashes mid-cycle and restarts? It could re-process and re-publish items that were already posted. There's no `mark_processed()` call shown in the agent's cycle flow.

**Fix:** `mark_processed(item_id)` must be called immediately after successful publish, and the agent loop must only call `fetch_latest_news()` with `unprocessed_only=True`.

#### 6. Website is listed as Week 4 — this is too late if Telegram needs it
If the brand is publishing breaking news to Telegram and linking to article URLs, the website must be live before Telegram posting starts. Links to a non-existent site will break trust.

**Fix:** Either (a) launch website before going live on Telegram, or (b) remove website links from Telegram messages until the site is live. Plan for this explicitly.

#### 7. No compliance / GDPR note for the website
If the website is public and indexable, especially with a news feed and user-facing content, there are basic legal hygiene items needed: cookie banner, privacy policy, terms of use. Minor but needs planning.

---

### 🟡 Important Missing Points

#### 8. No monitoring / observability
No logging strategy defined. No metrics collection. Once this runs autonomously, you need to know:
- How many items scraped per source per hour?
- What is the average score of published items?
- What is the publish success rate?
- What errors occurred?

**Fix:** Add structured logging (Python `logging` with JSON formatter) from day one. Use a free log aggregator (Logtail, Better Stack free tier, or just rotating log files + Telegram alerts).

#### 9. No secrets rotation plan
The `.env` file holds Telegram bot tokens, API keys, and broker credentials. No mention of how to rotate these if compromised. At minimum, note which keys need to be regenerated and how that affects running services.

#### 10. MT5 on Windows is not just a deployment note — it's a hard blocker
The ARCHITECTURE.md correctly calls this out, but the original implementation plan doesn't. The MT5 Python package requires a **live running MT5 terminal on Windows**. If the main server is Linux (as the docker-compose implies), you need a separate Windows VPS specifically for the MT5 adapter. This should be budgeted from day one.

#### 11. The FinancialJuice WebSocket approach needs a legal review before any code is written
The plan lists it as a source, flags the ToS risk, and then defers it to Week 5. The correct approach is: **do not write any FinancialJuice scraping code until you have read their API/data licensing terms** or found an alternative with a clear commercial license.

#### 12. No test for AI cost runaway
The brain runs on a cycle (every 15 minutes). If `agent.py` has a bug that causes it to loop or retry excessively, it can rack up significant AI API costs very fast. There is no mention of a per-day token budget cap or circuit breaker.

**Fix:** Add a `MAX_DAILY_API_CALLS` counter in `agent.py`. Alert and stop if it exceeds the limit.

#### 13. Telegram MTProto phone number not planned
Reading private or semi-public Telegram channels requires Telethon with a real phone number. The plan asks this as an open question but doesn't resolve it. If private channels are in scope, you need a dedicated phone number (SIM or VOIP) registered to a Telegram account used only for this bot — not your personal account.

---

## 6. APIs, Subscriptions & Credentials Needed

### 🔑 Required From Day One (Free)

| Service | What For | Cost | Where to Get |
|---|---|---|---|
| **Telegram Bot** (`@BotFather`) | Publishing to your Telegram channel | Free | `t.me/BotFather` |
| **Telegram Channel** | Your output channel | Free | Telegram app |
| **Google News RSS** | News source | Free | No signup needed |
| **Reuters RSS** | News source | Free | No signup needed |
| **Yahoo Finance RSS** | News source | Free | No signup needed |
| **GDELT Project API** | Real-time global news | Free | `gdeltproject.org` |
| **Supabase** | Postgres DB + Realtime for website | Free tier | `supabase.com` |
| **Vercel** | Website hosting (Next.js) | Free tier | `vercel.com` |
| **GitHub** | Code repo | Free | `github.com` |

---

### 🔑 Required for AI Brain

| Service | What For | Cost | Notes |
|---|---|---|---|
| **Anthropic API** (Claude) | Content brain rewrites, narrative scoring | ~$3–15/1M tokens (Sonnet) | You already have keys. Monitor usage daily. |
| **OR Google AI API** (Gemini) | Alternative AI brain | Free tier + pay-per-use | Gemini Flash is significantly cheaper for high-frequency tasks |

> [!IMPORTANT]
> **Recommendation:** Use **Gemini Flash** for the every-15-minute scoring/classify cycle (it's cheap and fast), and **Claude Sonnet** only for the final brand-voice rewrite before publishing. This keeps costs low without sacrificing quality on the content that actually gets posted.

---

### 🔑 Required for Video Character Workflow

| Service | What For | Cost | Notes |
|---|---|---|---|
| **HeyGen API** | Talking-head avatar video generation | ~$29–89/month (Creator/Business plan) | Each video render costs credits. 3×/day = ~90 videos/month minimum |
| **HyperFrames** | Top-half motion graphics | Pricing TBD — check current plan | Used for the visual half of each video |
| **FFmpeg** | Final video assembly (top + bottom halves) | Free, open source | Already installed on your machine |
| **ElevenLabs** (optional) | Voice synthesis if not using HeyGen voice | ~$22+/month | Only if you switch off HeyGen's built-in voice |

---

### 🔑 Required for Telegram Channel Reading (Private Channels)

| Service | What For | Cost | Notes |
|---|---|---|---|
| **Telegram API** (MTProto) | Reading private/semi-public Telegram channels via Telethon | Free | Requires `TELEGRAM_API_ID` + `TELEGRAM_API_HASH` from `my.telegram.org` |
| **Dedicated phone number** | Telethon session (do NOT use your personal number) | ~$5–10 one-time or VOIP | Use a burner SIM or a VOIP number (e.g., Google Voice, TextNow) |

> [!WARNING]
> Do not authenticate Telethon with your personal Telegram account. If the scraper gets flagged, Telegram can ban that account. Use a dedicated account tied to a separate number.

---

### 🔑 Required for Trading Engine

| Service | What For | Cost | Notes |
|---|---|---|---|
| **MT5 Demo Account** | Paper trading (Phase 2) | Free | Any MT5 broker — IC Markets, Pepperstone, etc. |
| **cTrader Demo Account** | Paper trading alternative | Free | IC Markets, Pepperstone also support cTrader |
| **Windows VPS** (for MT5) | MT5 terminal must run on Windows | ~$10–20/month | DigitalOcean Windows droplet or Vultr. Required if main server is Linux. |
| **NewsAPI.org** (optional) | Additional news source | Free: 100 req/day | `newsapi.org` — useful for keyword search |
| **Alpha Vantage** (optional) | News + market data | Free tier: 25 req/day | `alphavantage.co` |

---

### 🔑 Required for Production Deployment

| Service | What For | Cost | Notes |
|---|---|---|---|
| **Linux VPS** | Hosting collector + MCP + brain + DB + Redis | ~$6–20/month | Hetzner CX22 (€3.79/mo) or DigitalOcean Basic ($6/mo) — 2 vCPU, 4GB RAM is sufficient |
| **Upstash Redis** | Redis queue (managed, free tier) | Free up to 10K commands/day | `upstash.com` — use only if not self-hosting Redis on VPS |
| **Domain** (optional) | For the news website | ~$10–15/year | Namecheap, Cloudflare Registrar |
| **Cloudflare** (optional) | DNS + DDoS protection for website | Free tier | Works with Vercel |

---

## 7. Cost Breakdown

### Minimum Viable (Development, Local)

| Item | Monthly Cost |
|---|---|
| HeyGen Creator plan (3 videos/day) | ~$29 |
| Anthropic API (Claude Sonnet, ~90 rewrites/month) | ~$2–5 |
| All other sources | $0 |
| **Total MVP local** | **~$31–34/month** |

---

### Production (Self-Hosted VPS)

| Item | Monthly Cost |
|---|---|
| Linux VPS (Hetzner CX22) | ~€4 (~$4.50) |
| Windows VPS for MT5 (smallest Vultr instance) | ~$10 |
| HeyGen Business plan (3 videos/day + queue) | ~$89 |
| Anthropic API (Claude, mixed use) | ~$10–30 |
| Gemini Flash (high-frequency scoring cycles) | ~$1–5 |
| ElevenLabs (if used) | ~$22 |
| Domain (amortized monthly) | ~$1 |
| Supabase (free tier) | $0 |
| Upstash Redis (free tier) | $0 |
| Vercel (free tier) | $0 |
| **Total production (without ElevenLabs)** | **~$115–140/month** |
| **Total production (with ElevenLabs)** | **~$137–162/month** |

> [!TIP]
> **Biggest lever:** HeyGen is your largest cost. If you reduce to 1 video/day, the Creator plan ($29) works fine. At 3 videos/day with heavy use, look at the Business plan or negotiate an annual commitment for a discount.

> [!NOTE]
> **Indian Market specific (future Phase 4):** If you add Zerodha Kite Connect or Upstox for Indian algo trading, budget an additional ~₹2,000–5,000/month for broker API access + exchange data fees. This is a separate cost track and should not be mixed with the forex stack above.

---

## 8. Where Data Lives

| Data Type | Storage | Location | Notes |
|---|---|---|---|
| Raw scraped news items | SQLite (dev) → Postgres (prod) | `services/shared/db/` schema | `news_items` table with SHA-256 fingerprint |
| Processed/published flag | Same DB | `news_items.processed` column | Set by `mark_processed()` MCP tool |
| Trade decisions + outcomes | SQLite (dev) → Postgres (prod) | `services/trading-engine/trade_log/` | Full feature vector logged per trade for retraining |
| Source configuration | JSON file | `services/news-engine/collector/config/sources.json` | Defines all RSS URLs, Telegram channels, poll intervals |
| Brand voice + character rules | Markdown | `trending-news-character-skill-sanitized/SYSTEM.md` | Read by the AI brain on each cycle |
| Rendered videos | Local filesystem / cloud storage | `trending-news-character-skill-sanitized/output/` | Consider S3 or Supabase Storage for prod |
| Published Telegram message log | Postgres | `news_log` table | Used by social-distribution worker for daily recaps |
| Redis queue | Redis (in-memory) | `redis://localhost:6379` (dev), Upstash (prod) | Optional — SQLite is the default |
| ML model weights (Phase 3+) | Filesystem | `services/trading-engine/brain/` | Versioned by date, compared before promotion |
| Secrets / credentials | `.env` file | Repo root `.env` (gitignored) | Never commit. Copy from `.env.example` |

---

## 9. Deployment Options

### Option A — Local / Development (Start Here)
Run all services manually via PowerShell:
```powershell
# Terminal 1
python services/news-engine/collector/main.py

# Terminal 2
python services/news-engine/mcp_server/server.py

# Terminal 3
python services/news-engine/brain/agent.py

# Terminal 4 (website)
cd website && npm run dev
```

**Pros:** Zero cost, instant feedback, easy debugging  
**Cons:** Stops when machine sleeps, no auto-restart

---

### Option B — Cloud Production (Recommended for launch)

| Component | Host | Cost |
|---|---|---|
| Collector + MCP + Content Brain | Linux VPS (Hetzner/DigitalOcean) via Docker Compose | ~$4–6/mo |
| MT5 Adapter | Separate Windows VPS | ~$10/mo |
| Website | Vercel | Free |
| Database | Supabase (Postgres + Realtime) | Free |
| Redis | Upstash | Free |

**Docker Compose** (`infra/docker-compose.yml`) already covers all Linux-side services. The MT5 adapter is intentionally excluded and must run on Windows — point `MT5_MCP_URL` at it from the Linux stack.

---

### Option C — Single VPS (Simplest Ops)
Single Hetzner CX32 or DigitalOcean 4GB box:
- Docker Compose for all Linux services (collector, MCP, brain, Postgres, Redis, cTrader)
- PM2 or systemd as process supervisor
- Nginx reverse proxy for website if self-hosting
- MT5 still needs a separate Windows instance

---

## 10. Open Decisions (Unresolved)

These must be decided before build starts. They affect code paths, costs, and architecture.

| # | Decision | Options | Impact |
|---|---|---|---|
| **D1** | Primary AI provider for content brain | Claude Sonnet vs. Gemini Flash | Cost structure, API key routing |
| **D2** | News niche focus | Finance only / Crypto / General breaking / All | Determines `sources.json` config and keyword sets |
| **D3** | Telegram posting frequency | Fully auto (20–50/day) vs. curated (3–5/day) | Cycle interval in `agent.py`, HeyGen credit usage |
| **D4** | Private Telegram channels | Yes (need phone number + Telethon MTProto) vs. Public only | Infrastructure complexity, legal exposure |
| **D5** | Website domain | New domain vs. subdomain of existing | DNS setup, Vercel config |
| **D6** | Video trigger mechanism | `agent.py` calls a subprocess / HTTP endpoint to the skill folder vs. agent-to-agent call | Integration architecture of news brain → video character |
| **D7** | Rendered video storage | Local output folder vs. cloud (S3 / Supabase Storage) | Storage cost, CDN for website video embeds |
| **D8** | ElevenLabs voice | Use HeyGen built-in voice vs. ElevenLabs | +$22/month, better voice quality |
| **D9** | MT5 broker | IC Markets / Pepperstone / other | Determines demo account setup |
| **D10** | Indian market in scope? | Yes (separate SEBI compliance track) vs. not yet | Significant extra work, separate API stack |

---

## 11. Build Sequence Summary

This combines the v3 plan phases with the tradebrain roadmap into one ordered sequence:

```
PHASE 0 — FOUNDATION (Week 1)
  ✦ Set up tradebrain monorepo, Python venv, .env
  ✦ Shared Postgres/SQLite schema agreed and committed
  ✦ RSS scrapers running: Google News, Reuters, Yahoo Finance, GDELT
  ✦ Public Telegram channel scraper (httpx, no API key)
  ✦ SQLite queue with SHA-256 dedup working
  ✦ Run simulator.py — proves trading loop shape works on synthetic data
  ✦ Add error alerting (Telegram DM on service failure) — do this NOW not Week 5

PHASE 1 — NEWS MCP + CONTENT BRAIN (Week 2–3)
  ✦ FastMCP server: fetch / score / tag_category / summarize tools
  ✦ AI brain (agent.py) wired to Telegram + website publish tools
  ✦ mark_processed() called after every successful publish
  ✦ Full pipeline test: scraped item → Telegram message out
  ✦ Website (Next.js) live on Vercel with /api/news endpoint
  ✦ Resolve D1 (AI provider), D2 (niche), D3 (frequency) before this phase

PHASE 1B — VIDEO CHARACTER INTEGRATION (Week 3–4)
  ✦ Define how agent.py triggers the video character skill
  ✦ Wire news MCP selected story → video character workflow input
  ✦ 3×/day automated video: HeyGen avatar + HyperFrames + FFmpeg assembly
  ✦ Output goes to Telegram channel + website
  ✦ Resolve D6 (trigger mechanism) and D7 (video storage) before this phase

PHASE 2 — TRADING BRAIN ON PAPER (Week 3–5)
  ✦ MT5 demo account + MT5 MCP adapter (on Windows VPS)
  ✦ Decision engine: real news bias from MCP + technical rules → trade signal
  ✦ Every trade logged with full feature vector
  ✦ Target: 100–200+ logged demo trades before any judgment

PHASE 3 — RETRAINING + SOCIAL DISTRIBUTION (Week 5–6)
  ✦ Weekly retraining job: reads trade_log, refits scoring model
  ✦ Manual comparison of before/after before promoting new model
  ✦ Social distribution worker: daily recap from trade_log + news_log
  ✦ Add cTrader as second broker adapter

PHASE 4 — SCALE (Week 6–8+)
  ✦ Add FinancialJuice (only if ToS resolved)
  ✦ Add Telethon for private Telegram channels (only if D4 resolved)
  ✦ Add indices/CFDs in demo
  ✦ Indian market (only if D10 resolved — separate SEBI compliance track)

PHASE 5 — LIVE (After demo track record across multiple market regimes)
  ✦ Go live only after demo performance across >1 market condition
  ✦ Verify broker ToS permits automated/API trading
  ✦ Start at smallest position size allowed
```

---

## Appendix A — Key File Reference

| File | Purpose |
|---|---|
| [ARCHITECTURE.md](file:///C:/Beew/savage/tradebrain/tradebrain/ARCHITECTURE.md) | Canonical system design doc |
| [README.md](file:///C:/Beew/savage/tradebrain/tradebrain/README.md) | Repo quickstart |
| [docs/roadmap.md](file:///C:/Beew/savage/tradebrain/tradebrain/docs/roadmap.md) | Phased build sequence |
| [docs/simulation_guide.md](file:///C:/Beew/savage/tradebrain/tradebrain/docs/simulation_guide.md) | 3-stage path to live trading |
| [.env.example](file:///C:/Beew/savage/tradebrain/tradebrain/.env.example) | All environment variable templates |
| [requirements.txt](file:///C:/Beew/savage/tradebrain/tradebrain/requirements.txt) | Python dependencies |
| [infra/docker-compose.yml](file:///C:/Beew/savage/tradebrain/tradebrain/infra/docker-compose.yml) | Production Linux stack |
| [implementation_plan_news_collector](file:///C:/Beew/savage/trending-news-character-skill-v3/implementation_plan_news_collector) | Original news pipeline design doc |
| [SYSTEM.md](file:///C:/Beew/savage/trending-news-character-skill-v3/trending-news-character-skill-sanitized/SYSTEM.md) | Character brand voice + video rules |
| [AGENT_RUNBOOK.md](file:///C:/Beew/savage/trending-news-character-skill-v3/trending-news-character-skill-sanitized/AGENT_RUNBOOK.md) | Step-by-step agent execution guide |

---

## Appendix B — FinancialJuice ToS Status

FinancialJuice's live WebSocket (`wss://rt.financialjuice.com/connection/websocket`) is intended for authenticated browser users. **Do not build scraping code against it until:**
1. You have read their data licensing / API terms at `financialjuice.com`
2. Or you have a paid API access arrangement with them

Their RSS-style feeds and public website are lower risk but still worth checking. Start with Google News RSS, Reuters, GDELT, and public Telegram channels — all of which are safe starting sources.

---

*Document generated June 2026. Update this file as decisions in §10 are resolved and phases are completed.*
