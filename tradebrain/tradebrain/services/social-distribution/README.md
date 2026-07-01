# Social distribution

Reads from `trade_log` and `news_items` and posts scheduled recaps. Deliberately
has no broker credentials and no access to the trading or news MCP servers --
it's a read-only consumer of the two logs, kept on its own credentials
(`TELEGRAM_BOT_TOKEN` for a *different* channel than the news engine's, plus
`TWITTER_BEARER_TOKEN` once a second platform is added). This boundary is
intentional: a bug here should never be able to reach a broker.

## Open questions
- Which platforms beyond Telegram -- X/Twitter first, or also Discord?
- Recap cadence: daily only, or also a weekly "what the brain learned" post once Phase 3's retraining loop exists?
