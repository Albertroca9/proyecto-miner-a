"""Rank listings that meet explicit requirements by estimated list-price cost."""

import pandas as pd

from avance.data import INPUT_PRICE, OUTPUT_PRICE


def recommend(
    frame: pd.DataFrame,
    input_tokens: int,
    output_tokens: int,
    min_context: int,
    required_capabilities: list[str],
) -> pd.DataFrame:
    if min(input_tokens, output_tokens, min_context) < 0:
        raise ValueError("Token volumes and context must be nonnegative")
    missing = sorted(set(required_capabilities) - set(frame.columns))
    if missing:
        raise ValueError(f"Unknown capabilities: {', '.join(missing)}")

    eligible = frame.loc[pd.to_numeric(frame["max_input_tokens"], errors="coerce").ge(min_context)].copy()
    for capability in required_capabilities:
        eligible = eligible.loc[eligible[capability].eq(True)]
    eligible["estimated_cost_usd"] = (
        eligible[INPUT_PRICE] * input_tokens / 1_000_000
        + eligible[OUTPUT_PRICE] * output_tokens / 1_000_000
    )
    return eligible.sort_values(["estimated_cost_usd", "model_id"]).reset_index(drop=True)
