"""Daily cron-style entrypoint. Run with: python scheduler.py"""
import time
from datetime import datetime

from telegram_bot import build_daily_recap, post
from services.shared.utils.logger import get_logger

log = get_logger("social-scheduler")

POST_HOUR_UTC = 18  # adjust to taste


def fetch_todays_trades() -> list[dict]:
    # TODO: SELECT * FROM trades WHERE closed_at >= today
    return []


def fetch_todays_news_count() -> int:
    # TODO: SELECT count(*) FROM news_items WHERE published_at >= today
    return 0


def run_once():
    trades = fetch_todays_trades()
    news_count = fetch_todays_news_count()
    message = build_daily_recap(trades, news_count)
    post(message)


if __name__ == "__main__":
    log.info("social scheduler starting, posting daily at %s:00 UTC", POST_HOUR_UTC)
    last_posted_date = None
    while True:
        now = datetime.utcnow()
        if now.hour == POST_HOUR_UTC and now.date() != last_posted_date:
            run_once()
            last_posted_date = now.date()
        time.sleep(60)
