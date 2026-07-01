# Contributing

- One service per PR where possible — `services/news-engine`, `services/trading-engine`, `services/social-distribution`, `services/shared` are independently runnable.
- Anything that touches `services/trading-engine/mcp_server/` and could place a real order needs a second reviewer, no exceptions, even on a demo account.
- New env vars go in `.env.example` in the same PR that introduces them.
- Open questions belong in the relevant service's README under "Open questions" — resolve there before building further on top, so we're not all assuming different answers.
- Branch naming: `news/<thing>`, `trading/<thing>`, `social/<thing>`, `infra/<thing>`.
