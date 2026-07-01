"""
Weekly retraining skeleton (Phase 3+). Not needed to run the Stage 1
simulator. Reads trade_log, fits a model on (technical features + news bias)
-> outcome, and -- critically -- compares it against the currently deployed
model on the same held-out trades before anything gets promoted.

pip install scikit-learn pandas   # not in the base requirements.txt on purpose
"""
# import pandas as pd
# from sklearn.linear_model import LogisticRegression

def load_trade_features():
    """TODO: SELECT technical_signal, news_bias_score, news_category, outcome
    FROM trades WHERE outcome IN ('win','loss') -- needs ~100-200+ rows to mean
    anything, see docs/roadmap.md Phase 2."""
    raise NotImplementedError


def fit_candidate_model(features):
    """TODO: fit on the feature set above, return both the model and its
    held-out accuracy / win-rate so it can be compared, not blindly trusted."""
    raise NotImplementedError


def compare_against_deployed(candidate, deployed_model_version: str) -> bool:
    """TODO: backtest the candidate against the same held-out trades the
    deployed model was scored on. Return True only if it's a genuine
    improvement, not noise. A human should see this comparison before
    promotion -- don't auto-deploy."""
    raise NotImplementedError


if __name__ == "__main__":
    print("train.py is a Phase 3 skeleton -- see docstrings, not runnable yet.")
