"""Posts a formatted recap to a Telegram channel. Read-only against the
shared DB -- never imports anything from trading-engine/mcp_server or
news-engine beyond reading their log tables."""
from services.shared.config.settings import settings
from services.shared.utils.logger import get_logger

log = get_logger("social-telegram")


def build_daily_recap(trades: list[dict], news_count: int) -> str:
    if not trades:
        return "No trades closed today."
    wins = sum(1 for t in trades if t.get("outcome") == "win")
    total = len(trades)
    pnl = sum(t.get("pnl", 0) for t in trades)
    return (
        f"\U0001F4CA Daily recap\n\n"
        f"Trades: {total} | Win rate: {wins/total:.0%}\n"
        f"PnL: {pnl:.5f}\n"
        f"News items scanned: {news_count}\n"
    )


def post(message: str) -> None:
    if not settings.telegram_bot_token:
        log.warning("TELEGRAM_BOT_TOKEN not set, skipping post: %s", message)
        return
    # TODO: python-telegram-bot send_message call here
    log.info("posted: %s", message)
