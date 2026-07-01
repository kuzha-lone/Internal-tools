# Telegram Real-Time News Bot

Fetches breaking news from multiple sources and posts to your Telegram channel in real time.

## Setup (3 steps)

### Step 1 — Create .env
```
cp .env.example .env
```
Fill in:
- `TELEGRAM_BOT_TOKEN` — get from [@BotFather](https://t.me/BotFather) → `/newbot`
- `TELEGRAM_CHANNEL_ID` — your channel (e.g. `@mychannel` or numeric `-100xxxxxxxx`)

### Step 2 — Test the scanner (no Telegram needed)
```
python test_scanner.py
```
If you see articles printed — the scanner works ✅

### Step 3 — Start the bot
```
python main.py
```

## Configuration

| File | Purpose |
|---|---|
| `config/settings.json` | Scan interval, max per run, age filter, keywords |
| `config/sources.json` | RSS feeds to monitor |
| `.env` | API keys |

## News Sources (all free, no API key)
- Reuters World + Business
- BBC World + Technology  
- CNBC Top News
- Al Jazeera
- Hacker News
- CoinDesk
- Reddit WorldNews
- Google News

## Optional API Keys
Add to `.env` for more sources:
- `GNEWS_API_KEY` — [gnews.io](https://gnews.io) (100 req/day free)
- `NEWSAPI_KEY` — [newsapi.org](https://newsapi.org) (100 req/day free)

## Message Format
```
🌍 **Breaking: Title of the News**

Summary of the article in one line.

🔗 Read full article
📡 Reuters  ·  🕐 12 min ago
```

## Stopping the Bot
Press `Ctrl+C`
