"""
Single place every service loads its config from, so an env var added for
one service is visible (and documented in .env.example) for all of them.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///trade_log.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_channel_id: str = os.getenv("TELEGRAM_CHANNEL_ID", "")

    mt5_login: str = os.getenv("MT5_LOGIN", "")
    mt5_password: str = os.getenv("MT5_PASSWORD", "")
    mt5_server: str = os.getenv("MT5_SERVER", "")
    mt5_account_type: str = os.getenv("MT5_ACCOUNT_TYPE", "demo")

    ctrader_client_id: str = os.getenv("CTRADER_CLIENT_ID", "")
    ctrader_client_secret: str = os.getenv("CTRADER_CLIENT_SECRET", "")
    ctrader_account_type: str = os.getenv("CTRADER_ACCOUNT_TYPE", "demo")

    def assert_not_live_by_accident(self) -> None:
        """Call this before any code path that can place a real order."""
        if self.mt5_account_type == "live" or self.ctrader_account_type == "live":
            print("WARNING: account_type is set to 'live'. Confirm this is intentional.")


settings = Settings()
