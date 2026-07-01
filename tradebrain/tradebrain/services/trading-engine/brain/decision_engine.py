"""
The trading brain's scoring logic. Deliberately a transparent rule-based
combiner, not a black-box model -- this is what gets logged, audited, and
eventually (Phase 3) replaced piece by piece with something learned from
trade_log, one swap at a time, compared against this baseline before promotion.
"""
from dataclasses import dataclass


@dataclass
class NewsBias:
    category: str          # crypto | currency | economy
    sentiment_score: float  # -1.0 .. 1.0
    impact_score: float     # 0..100


@dataclass
class TechnicalSignal:
    symbol: str
    fast_ma: float
    slow_ma: float
    trend: str  # "up" | "down" | "flat"


@dataclass
class TradeSignal:
    symbol: str
    action: str       # "long" | "short" | "flat"
    confidence: float  # 0.0 .. 1.0
    reasoning: str


MODEL_VERSION = "rule-v1"


def score_trade_idea(technical: TechnicalSignal, news: NewsBias | None) -> TradeSignal:
    """v1 rule: trade with the technical trend, but only if news bias doesn't
    actively disagree. No news available -> trade on technicals alone with
    reduced confidence."""
    if technical.trend == "flat":
        return TradeSignal(technical.symbol, "flat", 0.0, "no clear technical trend")

    technical_action = "long" if technical.trend == "up" else "short"

    if news is None:
        return TradeSignal(technical.symbol, technical_action, 0.4,
                            "technical trend only, no news bias available")

    news_agrees = (
        (technical_action == "long" and news.sentiment_score >= 0) or
        (technical_action == "short" and news.sentiment_score <= 0)
    )
    if not news_agrees and news.impact_score > 60:
        return TradeSignal(technical.symbol, "flat", 0.0,
                            f"technical said {technical_action} but high-impact news disagrees")

    confidence = 0.5 + (0.3 if news_agrees else 0.0) + (news.impact_score / 1000)
    return TradeSignal(technical.symbol, technical_action, min(confidence, 0.95),
                        f"technical {technical_action}, news {'agrees' if news_agrees else 'neutral/low-impact'}")


if __name__ == "__main__":
    # quick manual sanity check
    tech = TechnicalSignal(symbol="EURUSD", fast_ma=1.0865, slow_ma=1.0840, trend="up")
    news = NewsBias(category="currency", sentiment_score=0.4, impact_score=70)
    print(score_trade_idea(tech, news))
