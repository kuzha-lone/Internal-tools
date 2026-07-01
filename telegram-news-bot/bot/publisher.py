"""
publisher.py — Formats news articles and sends them to the Telegram channel.
Uses python-telegram-bot in async mode.
"""

import asyncio
import os
from datetime import datetime, timezone
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

# Category emoji map
CATEGORY_EMOJI = {
    "world":      "🌍",
    "markets":    "📈",
    "technology": "💻",
    "crypto":     "₿",
    "politics":   "🏛️",
    "general":    "📰",
    "science":    "🔬",
    "health":     "🏥",
    "sports":     "⚽",
}


def _age_label(age_hours: float) -> str:
    if age_hours < 1:
        minutes = int(age_hours * 60)
        return f"{minutes} min ago"
    elif age_hours < 24:
        return f"{int(age_hours)}h ago"
    else:
        return f"{int(age_hours // 24)}d ago"


def format_message(article: dict) -> str:
    """
    Build the Telegram message string for one article.
    Uses HTML parse mode for bold/links.
    """
    category = article.get("category", "general")
    emoji = CATEGORY_EMOJI.get(category, "📰")
    age = _age_label(article.get("age_hours", 0))
    source = article.get("source", "Unknown")
    title = article.get("title", "No title")
    summary = article.get("summary", "")
    url = article.get("url", "")

    lines = [
        f"{emoji} <b>{title}</b>",
        f"",
        f"🔗 <a href=\"{url}\">Read full article</a>",
        f"📡 {source}  ·  🕐 {age}",
    ]

    if summary:
        # Trim summary to a clean sentence
        clean = summary.split(".")[0].strip()
        if len(clean) > 20:
            lines.insert(2, f"")
            lines.insert(3, f"<i>{clean}.</i>")

    return "\n".join(lines)


async def send_article(bot: Bot, channel_id: str, article: dict) -> bool:
    """
    Send a single article to the Telegram channel.
    Returns True on success, False on failure.
    """
    message = format_message(article)
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
        )
        print(f"[publisher] Sent: {article['title'][:60]}")
        return True
    except TelegramError as e:
        print(f"[publisher] Telegram error: {e}")
        return False
    except Exception as e:
        print(f"[publisher] Unexpected error: {e}")
        return False


async def send_batch(bot: Bot, channel_id: str, articles: list, delay_seconds: float = 2.0):
    """
    Send multiple articles with a delay between each to avoid flooding.
    """
    sent = 0
    for article in articles:
        ok = await send_article(bot, channel_id, article)
        if ok:
            sent += 1
        # Telegram rate limit: ~30 msgs/sec max, we stay well under
        await asyncio.sleep(delay_seconds)
    print(f"[publisher] Batch complete — {sent}/{len(articles)} articles sent")
    return sent


async def send_startup_message(bot: Bot, channel_id: str):
    """Send a startup notification to the channel."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    msg = (
        "🤖 <b>News Bot Online</b>\n\n"
        f"📡 Real-time news feed activated\n"
        f"🕐 Started at {now}\n\n"
        "<i>Scanning Reuters, BBC, CNBC, Al Jazeera, CoinDesk and more...</i>"
    )
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=msg,
            parse_mode=ParseMode.HTML,
        )
        print("[publisher] Startup message sent")
    except Exception as e:
        print(f"[publisher] Could not send startup message: {e}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    channel = os.getenv("TELEGRAM_CHANNEL_ID", "")
    if not token or not channel:
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env first")
    else:
        test_article = {
            "title": "Test Article — Bot is working!",
            "summary": "This is a test message from the Telegram news bot.",
            "url": "https://example.com",
            "source": "Test Source",
            "category": "general",
            "age_hours": 0.1,
        }
        bot = Bot(token=token)
        asyncio.run(send_article(bot, channel, test_article))
