"""
main.py — Entry point for the Telegram Real-Time News Bot.

What it does:
  1. Loads config and API keys from .env
  2. Scans RSS feeds + optional APIs every N minutes (default: 10 min)
  3. Filters out already-seen stories
  4. Sends new stories to the configured Telegram channel
  5. Marks stories as seen to prevent duplicates

Usage:
  python main.py

Stop:
  Ctrl+C
"""

import asyncio
import io
import json
import os
import sys
from pathlib import Path

# Force UTF-8 output on Windows (emoji-safe console)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Resolve paths
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# Load .env from the bot root directory
load_dotenv(ROOT / ".env")

from research.scanner import fetch_all
from research.deduplicator import filter_new, mark_seen
from bot.publisher import send_batch, send_startup_message

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────

def load_settings() -> dict:
    settings_path = ROOT / "config" / "settings.json"
    with open(settings_path) as f:
        return json.load(f)


SETTINGS = load_settings()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
SCAN_INTERVAL = SETTINGS.get("scan_interval_minutes", 10)
MAX_PER_RUN = SETTINGS.get("max_articles_per_run", 5)
DEDUP_TTL = SETTINGS.get("dedup_ttl_hours", 24)

# ──────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────

def validate_config():
    if not BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN is not set in .env")
        print("   → Go to @BotFather on Telegram and create a bot")
        sys.exit(1)
    if not CHANNEL_ID:
        print("❌ ERROR: TELEGRAM_CHANNEL_ID is not set in .env")
        print("   → Set it to @yourchannel or the numeric -100xxxxxxxxxx ID")
        sys.exit(1)
    print("✅ Config OK")
    print(f"   Channel : {CHANNEL_ID}")
    print(f"   Interval: every {SCAN_INTERVAL} minutes")
    print(f"   Max/run : {MAX_PER_RUN} articles")

# ──────────────────────────────────────────────
# Core scan + publish cycle
# ──────────────────────────────────────────────

async def run_scan_cycle(bot: Bot):
    print(f"\n[main] ── Scan cycle started ──")

    # 1. Fetch articles from all sources
    all_articles = fetch_all()
    if not all_articles:
        print("[main] No articles fetched this cycle")
        return

    # 2. Filter out already-posted stories
    new_articles = filter_new(all_articles, ttl_hours=DEDUP_TTL)
    print(f"[main] {len(new_articles)} new (unseen) articles")

    if not new_articles:
        print("[main] Nothing new to post")
        return

    # 3. Cap how many we send per run (avoid flooding the channel)
    to_send = new_articles[:MAX_PER_RUN]

    # 4. Send to Telegram
    sent = await send_batch(bot, CHANNEL_ID, to_send, delay_seconds=2.0)

    # 5. Mark sent articles as seen
    for article in to_send[:sent]:
        mark_seen(article.get("id", article.get("url", "")), article.get("title", ""))

    print(f"[main] Cycle done — {sent} articles posted")

# ──────────────────────────────────────────────
# Main entrypoint
# ──────────────────────────────────────────────

async def main():
    validate_config()

    bot = Bot(token=BOT_TOKEN)

    # Verify bot is reachable
    try:
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        sys.exit(1)

    # Send startup notice to channel
    await send_startup_message(bot, CHANNEL_ID)

    # Run first scan immediately
    await run_scan_cycle(bot)

    # Schedule recurring scans
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_scan_cycle,
        "interval",
        minutes=SCAN_INTERVAL,
        args=[bot],
        id="news_scan",
    )
    scheduler.start()
    print(f"\n🟢 Bot running — scanning every {SCAN_INTERVAL} min")
    print("   Press Ctrl+C to stop\n")

    # Keep alive
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("\n🔴 Bot stopped")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
