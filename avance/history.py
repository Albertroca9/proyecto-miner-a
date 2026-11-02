"""Historical cohort and descriptive weekly price summaries."""

import pandas as pd

from avance.data import INPUT_PRICE, OUTPUT_PRICE


def prepare_history(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"week_start", "model_id", "mode", INPUT_PRICE, OUTPUT_PRICE}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    result = frame.copy()
    result["week_start"] = pd.to_datetime(result["week_start"], errors="coerce")
    for column in (INPUT_PRICE, OUTPUT_PRICE):
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result.loc[
        result["mode"].eq("chat")
        & result["week_start"].notna()
        & result[INPUT_PRICE].gt(0)
        & result[OUTPUT_PRICE].gt(0)
    ].copy()
    return result.reset_index(drop=True)


def weekly_summary(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.groupby("week_start", as_index=False).agg(
        n_listings=("model_id", "size"),
        median_input_usd=(INPUT_PRICE, "median"),
        median_output_usd=(OUTPUT_PRICE, "median"),
    )
    return result.sort_values("week_start").reset_index(drop=True)


def price_changes(frame: pd.DataFrame, column: str) -> dict[str, int]:
    if column not in (INPUT_PRICE, OUTPUT_PRICE):
        raise ValueError("Choose an input or output token price column")
    ordered = frame.sort_values(["model_id", "week_start"])
    previous = ordered.groupby("model_id")[column].shift()
    compared = ordered.loc[previous.notna()].copy()
    compared["previous"] = previous.loc[previous.notna()]
    changed = compared.loc[compared[column].ne(compared["previous"])]
    return {
        "comparisons": len(compared),
        "changes": len(changed),
        "decreases": int(changed[column].lt(changed["previous"]).sum()),
        "increases": int(changed[column].gt(changed["previous"]).sum()),
        "models_changed": changed["model_id"].nunique(),
    }
