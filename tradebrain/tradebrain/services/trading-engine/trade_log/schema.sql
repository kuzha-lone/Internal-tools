-- Local sqlite mirror of services/shared/db/schema.sql's `trades` table,
-- used by simulator.py and early MT5/cTrader testing before this becomes
-- shared Postgres infra.
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    broker TEXT,
    symbol TEXT,
    side TEXT,
    qty REAL,
    entry_price REAL,
    exit_price REAL,
    opened_at TEXT,
    closed_at TEXT,
    pnl REAL,
    outcome TEXT,                 -- win | loss | open
    news_bias_score REAL,
    news_category TEXT,
    technical_signal TEXT,        -- json blob
    confidence REAL,
    model_version TEXT
);
