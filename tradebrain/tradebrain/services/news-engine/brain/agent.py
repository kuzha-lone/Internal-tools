"""
Content brain: pulls top news items, scores + categorizes + rewrites them,
and publishes. This file is the agent LOOP -- the actual LLM call and the
publish_to_telegram / publish_to_website tools are deliberately left as
TODOs since they depend on which AI provider and which channel/site are
finalized (see README open questions).
"""
import time
from services.shared.utils.logger import get_logger

log = get_logger("content-brain")

CYCLE_SECONDS = 900  # every 15 minutes, per the original plan's cadence


def run_cycle():
    # TODO: call news MCP server's fetch_latest_news()
    # TODO: for each item, call score_narrative() + tag_category()
    # TODO: pick top 1-3 by impact_score
    # TODO: call summarize_news() in brand voice
    # TODO: call publish_to_telegram() / publish_to_website()
    log.info("cycle ran (stub) -- wire up MCP client calls here")


if __name__ == "__main__":
    log.info("content brain starting, cycle every %ss", CYCLE_SECONDS)
    while True:
        run_cycle()
        time.sleep(CYCLE_SECONDS)
