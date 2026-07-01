"""
Stage 1 simulator: stdlib only, no broker, no API keys, no internet. Proves
the signal -> decision -> log -> stats loop works before anything real is
connected. Run: python simulator.py

The price series is a random walk and mock_news_bias() is random noise --
results here say NOTHING about real trading performance. The point is to
exercise the pipeline shape, not to evaluate a strategy.

Replace, in order, as the roadmap progresses:
  1. mock_news_bias()      -> real call to the news MCP server's score_narrative
  2. generate_synthetic_prices() -> real historical OHLC data for a real backtest
  3. SimpleBroker            -> the MT5/cTrader MCP adapters for a live demo account
"""
import random
import sqlite3
import statistics
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

DB_PATH = "trade_log.db"
SYMBOL = "EURUSD"
N_TICKS = 2000
FAST_WINDOW = 10
SLOW_WINDOW = 40


# ---------- synthetic data (replace with real OHLC later) ----------

def generate_synthetic_prices(n: int, start: float = 1.0850, seed: int = 42) -> list[float]:
    random.seed(seed)
    prices = [start]
    for _ in range(n - 1):
        drift = random.gauss(0, 0.0006)
        prices.append(round(prices[-1] + drift, 5))
    return prices


def mock_news_bias() -> float:
    """Placeholder for the real score_narrative MCP tool. Returns sentiment
    in -1..1, weighted slightly toward neutral to mimic real news flow."""
    return round(random.gauss(0, 0.35), 2)


# ---------- technical signal ----------

def moving_average(values: list[float]) -> float:
    return sum(values) / len(values)


def trend_from_window(prices: list[float], i: int) -> str | None:
    if i < SLOW_WINDOW:
        return None
    fast = moving_average(prices[i - FAST_WINDOW:i])
    slow = moving_average(prices[i - SLOW_WINDOW:i])
    if fast > slow * 1.0002:
        return "up"
    if fast < slow * 0.9998:
        return "down"
    return "flat"


# ---------- decision (mirrors brain/decision_engine.py's logic, kept
# inline here so this file has zero imports and zero setup) ----------

@dataclass
class SimTrade:
    side: str
    entry_price: float
    entry_index: int
    news_bias_at_entry: float
    confidence: float


def decide(trend: str | None, news_bias: float) -> tuple[str, float]:
    if trend is None or trend == "flat":
        return "flat", 0.0
    technical_action = "long" if trend == "up" else "short"
    news_agrees = (technical_action == "long" and news_bias >= 0) or \
                  (technical_action == "short" and news_bias <= 0)
    if not news_agrees and abs(news_bias) > 0.5:
        return "flat", 0.0
    confidence = 0.5 + (0.3 if news_agrees else 0.0)
    return technical_action, confidence


# ---------- trade log ----------

def init_db(path: str = DB_PATH) -> None:
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT, side TEXT, entry_price REAL, exit_price REAL,
                pnl REAL, outcome TEXT, news_bias_at_entry REAL,
                confidence REAL, opened_at TEXT, closed_at TEXT
            )
        """)
        conn.commit()


def log_trade(trade: SimTrade, exit_price: float, opened_at: datetime, closed_at: datetime, path: str = DB_PATH) -> float:
    pnl = (exit_price - trade.entry_price) if trade.side == "long" else (trade.entry_price - exit_price)
    outcome = "win" if pnl > 0 else "loss"
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            "INSERT INTO trades (symbol, side, entry_price, exit_price, pnl, outcome, "
            "news_bias_at_entry, confidence, opened_at, closed_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (SYMBOL, trade.side, trade.entry_price, exit_price, pnl, outcome,
             trade.news_bias_at_entry, trade.confidence, opened_at.isoformat(), closed_at.isoformat())
        )
        conn.commit()
    return pnl


# ---------- main loop ----------

def run_simulation():
    init_db()
    prices = generate_synthetic_prices(N_TICKS)
    start_time = datetime.now(timezone.utc)

    open_trade: SimTrade | None = None
    hold_bars = 0
    MAX_HOLD = 20
    pnls: list[float] = []

    for i, price in enumerate(prices):
        now = start_time + timedelta(minutes=i)

        if open_trade is not None:
            hold_bars += 1
            current_trend = trend_from_window(prices, i)
            should_exit = hold_bars >= MAX_HOLD or current_trend == "flat" or current_trend is None
            if should_exit:
                pnl = log_trade(open_trade, price, start_time + timedelta(minutes=open_trade.entry_index), now)
                pnls.append(pnl)
                open_trade = None
                hold_bars = 0
            continue

        trend = trend_from_window(prices, i)
        news_bias = mock_news_bias()
        action, confidence = decide(trend, news_bias)
        if action != "flat":
            open_trade = SimTrade(action, price, i, news_bias, confidence)
            hold_bars = 0

    print_summary(pnls)


def print_summary(pnls: list[float]) -> None:
    if not pnls:
        print("No trades closed in this run.")
        return
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    print(f"--- Simulation summary ({SYMBOL}, {len(pnls)} trades, synthetic data) ---")
    print(f"Win rate:        {len(wins) / len(pnls):.1%}")
    print(f"Total PnL:       {sum(pnls):.5f}")
    print(f"Avg win:         {statistics.mean(wins):.5f}" if wins else "Avg win:         n/a")
    print(f"Avg loss:        {statistics.mean(losses):.5f}" if losses else "Avg loss:        n/a")
    print(f"Logged to:       {DB_PATH}")
    print("\nReminder: synthetic random-walk prices and random news bias. This")
    print("number means nothing about real performance -- it only proves the")
    print("signal -> decision -> log -> stats loop runs end to end.")


if __name__ == "__main__":
    run_simulation()
