"""Select comparable token-priced chat listings from the current catalogue."""

import pandas as pd


INPUT_PRICE = "input_price_per_1m_tokens"
OUTPUT_PRICE = "output_price_per_1m_tokens"
EXAMPLE_OUTPUT_SHARE = 0.25


def prepare_snapshot(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"model_id", "mode", INPUT_PRICE, OUTPUT_PRICE}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    result = frame.copy()
    for column in (INPUT_PRICE, OUTPUT_PRICE):
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result.loc[
        result["mode"].eq("chat")
        & result[INPUT_PRICE].gt(0)
        & result[OUTPUT_PRICE].gt(0)
    ].copy()
    result["example_cost_usd"] = result[INPUT_PRICE] + EXAMPLE_OUTPUT_SHARE * result[OUTPUT_PRICE]
    return result.reset_index(drop=True)
