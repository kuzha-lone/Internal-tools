"""
cTrader broker adapter via the Open API (OAuth-based, REST/protobuf). Unlike
the MT5 adapter, this has no Windows-terminal requirement and runs fine in
the same Linux stack as everything else.

DEMO ACCOUNT ONLY until the team has agreed the demo results justify going
live -- see docs/roadmap.md.
"""
from fastmcp import FastMCP
from services.shared.config.settings import settings

mcp = FastMCP("ctrader-adapter")


def _ensure_connected():
    settings.assert_not_live_by_accident()
    # TODO: OAuth flow with CTRADER_CLIENT_ID / CTRADER_CLIENT_SECRET,
    # then open the protobuf/REST session for CTRADER_ACCOUNT_ID.
    raise NotImplementedError("Wire up the cTrader Open API client first.")


@mcp.tool()
def place_order(symbol: str, side: str, qty: float, confidence: float = 0.0, reasoning: str = "") -> dict:
    """Same interface as the MT5 adapter's place_order -- the brain doesn't
    need to know which broker it's calling."""
    _ensure_connected()
    raise NotImplementedError


@mcp.tool()
def get_positions() -> list[dict]:
    _ensure_connected()
    raise NotImplementedError


@mcp.tool()
def close_position(position_id: str) -> dict:
    _ensure_connected()
    raise NotImplementedError


@mcp.tool()
def get_account_state() -> dict:
    _ensure_connected()
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()
