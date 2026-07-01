# Simulation guide

Three stages, in order. Don't skip a stage to get to "real" trading faster — each one is what makes the next stage's results trustworthy.

## Stage 1 — Synthetic simulation (today, no accounts needed)

```bash
python services/trading-engine/backtester/simulator.py
```

This generates a synthetic price walk, runs a simple moving-average crossover technical rule combined with a mock news bias score, logs every simulated trade to `trade_log.db`, and prints a win rate / total PnL summary at the end. Its only purpose is to prove the loop's shape (signal -> decision -> log -> stats) works before anything real is connected. Expect the results to mean nothing about real performance — the price series is random.

Replace `mock_news_bias()` in `simulator.py` with a real call to the news MCP server's `score_narrative` tool once Phase 1 of the roadmap is done, and replace the synthetic price generator with historical OHLC data once you want a real backtest rather than a loop test.

## Stage 2 — MT5 demo account (forex first)

1. Open a free demo account with any MT5-supporting broker (no money, no KYC needed for most brokers' demo accounts).
2. Fill in `MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER` in `.env`.
3. Run the MT5 MCP server (`services/trading-engine/mcp_server/mt5_server.py`) — note it requires a running MT5 terminal, which means Windows (or Wine). See `ARCHITECTURE.md` for why this affects server placement.
4. Point the decision engine at it instead of the simulator's mock execution.
5. Let it accumulate at least 100-200 logged trades before drawing any conclusion about whether the news-bias + technical-rule combination is actually adding value over technical rules alone. Compare both, don't just trust the combined number.

## Stage 3 — Live, smallest size

Only after Stage 2 has run across more than one distinct market condition (not just one trending week). Confirm the broker's terms permit automated/API trading on the account type you're using, and start at the smallest size the broker allows. Demo performance is informative, not predictive — slippage, execution latency, and the psychology of real money all change the picture.

## A note on the Indian market specifically

If/when the team wants Indian equities or F&O in the mix, treat it as its own track rather than folding it into the forex stack above. SEBI's retail algo trading framework (finalized through 2025, mandatory for all brokers from April 2026) requires API-driven strategies above a 10 orders/second threshold to be registered and routed through the broker with an exchange-issued strategy ID. Below that threshold you're a "regular API user" with lighter requirements. Either way, plan for broker empanelment (Zerodha Kite Connect, Upstox, etc.) as a separate piece of work, not something that falls out of the MT5/cTrader adapters for free.
