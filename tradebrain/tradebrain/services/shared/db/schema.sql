-- Shared schema. SQLite-compatible subset is used by the simulator for local
-- dev; this Postgres version is what the team's shared environment runs.

CREATE TABLE IF NOT EXISTS news_items (
    id              TEXT PRIMARY KEY,           -- sha256 of headline, dedup key
    source          TEXT NOT NULL,
    headline        TEXT NOT NULL,
    body            TEXT,
    category        TEXT,                       -- crypto | currency | economy | other
    sentiment_score REAL,                        -- -1.0 .. 1.0
    impact_score    INTEGER,                      -- 0..100, virality/urgency
    published_at    TIMESTAMPTZ NOT NULL,
    processed       BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS trades (
    id                  SERIAL PRIMARY KEY,
    broker              TEXT NOT NULL,            -- mt5 | ctrader
    symbol              TEXT NOT NULL,
    side                TEXT NOT NULL,             -- long | short
    qty                 REAL NOT NULL,
    entry_price         REAL NOT NULL,
    exit_price          REAL,
    opened_at           TIMESTAMPTZ NOT NULL,
    closed_at           TIMESTAMPTZ,
    pnl                 REAL,
    outcome             TEXT,                       -- win | loss | open
    news_bias_score     REAL,                        -- sentiment input at decision time
    news_category       TEXT,
    technical_signal    JSONB,                        -- whatever features fed the decision
    confidence          REAL,                          -- 0.0 .. 1.0, model's own confidence
    model_version        TEXT                            -- which brain version made the call
);

CREATE TABLE IF NOT EXISTS account_snapshots (
    id          SERIAL PRIMARY KEY,
    broker      TEXT NOT NULL,
    equity      REAL NOT NULL,
    balance     REAL NOT NULL,
    taken_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_news_category ON news_items(category);
CREATE INDEX IF NOT EXISTS idx_trades_outcome ON trades(outcome);
