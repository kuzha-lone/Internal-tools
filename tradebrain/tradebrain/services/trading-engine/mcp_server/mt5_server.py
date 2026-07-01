"""
MT5 broker adapter, exposed as MCP tools the trading brain calls.

REQUIRES a running MT5 terminal -- the official `MetaTrader5` python package
only talks to a local terminal instance, and that terminal is Windows-native.
Run this file ON Windows (or a Wine setup you trust), not on the same Linux
box as the rest of docker-compose.yml. See ARCHITECTURE.md.

DEMO ACCOUNT ONLY until the team has agreed the simulator + demo results
justify moving to live -- see docs/roadmap.md.
"""
from fastmcp import FastMCP
from services.shared.config.settings import settings

mcp = FastMCP("mt5-adapter")

# import MetaTrader5 as mt5   # uncomment once running on the Windows box


def _ensure_connected():
    settings.assert_not_live_by_accident()
    # TODO: mt5.initialize(login=int(settings.mt5_login),
    #                       password=settings.mt5_password,
    #                       server=settings.mt5_server)
    raise NotImplementedError("Wire up the MetaTrader5 package on the Windows host first.")


@mcp.tool()
def place_order(symbol: str, side: str, qty: float, confidence: float = 0.0, reasoning: str = "") -> dict:
    """Place a market order. side is 'long' or 'short'. Every call here
    should correspond to a row written to the trades table -- log first,
    or alongside, never after."""
    _ensure_connected()
    # TODO: build mt5.order_send() request, log to trade_log on success
    raise NotImplementedError


@mcp.tool()
def get_positions() -> list[dict]:
    """Return currently open positions."""
    _ensure_connected()
    # TODO: mt5.positions_get()
    raise NotImplementedError


@mcp.tool()
def close_position(ticket: int) -> dict:
    """Close a specific open position by its ticket id."""
    _ensure_connected()
    raise NotImplementedError


@mcp.tool()
def get_account_state() -> dict:
    """Return balance, equity, margin -- used for account_snapshots logging."""
    _ensure_connected()
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()
