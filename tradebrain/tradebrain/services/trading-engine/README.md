# Trading engine

The decision brain plus broker adapters. Start here: `python backtester/simulator.py` runs end-to-end on synthetic data with zero setup — see `docs/simulation_guide.md` at the repo root for the full three-stage path to live.

## Layout
```
trading-engine/
├── mcp_server/
│   ├── mt5_server.py       # MT5 adapter -- needs a running MT5 terminal (Windows)
│   └── ctrader_server.py   # cTrader adapter -- OAuth REST, runs anywhere
├── brain/
│   ├── decision_engine.py  # combines news bias + technical rules into a signal
│   └── train.py             # weekly retraining job, reads trade_log
├── backtester/
│   └── simulator.py         # stdlib-only paper trading loop, run today
└── trade_log/
    └── schema.sql            # local sqlite mirror of services/shared/db/schema.sql
```

## Platform note that affects server planning
`MetaTrader5` (the official Python package) only talks to a running MT5 terminal, and that terminal is Windows-native. If the rest of the stack runs on Linux (as `infra/docker-compose.yml` assumes), the MT5 adapter needs its own Windows VPS/VM exposing its MCP server over the network — it isn't a container you can drop into the same compose file. cTrader's Open API has no such constraint.

## TradingView
No public order-execution API for arbitrary accounts. Use Pine Script alerts/webhooks as an additional technical signal feeding `decision_engine.py`, not as an execution path.

## Open questions
- Which broker for the first MT5 demo account?
- Initial instrument scope: majors only, or majors + a couple of indices from the start?
- Who owns the weekly retraining review (Phase 3) -- someone needs to eyeball the before/after comparison before a new model version is promoted.
