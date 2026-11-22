"""Out-of-time price evaluation and weekly catalogue dynamics."""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from avance.data import INPUT_PRICE, OUTPUT_PRICE


def catalog_dynamics(frame):
    """Compare eligible listing sets in successive observed calendar weeks."""
    ordered = frame.sort_values(["week_start", "model_id"])
    weeks = sorted(ordered.week_start.unique())
    rows = []
    previous = None
    for week in weeks:
        current = ordered.loc[ordered.week_start.eq(week)].set_index("model_id")
        if not current.index.is_unique:
            raise ValueError("model_id must be unique within each week")
        current_ids = set(current.index)
        prior_ids = set() if previous is None else set(previous.index)
        common = current_ids & prior_ids
        entrants = current_ids - prior_ids
        exits = prior_ids - current_ids
        common_index = sorted(common)
        rows.append({
            "week_start": week,
            "n_listings": len(current_ids),
            "entrants": len(entrants),
            "continuers": len(common),
            "exits": len(exits),
            "input_price_changes": 0 if previous is None else int(
                current.loc[common_index, INPUT_PRICE].ne(previous.loc[common_index, INPUT_PRICE]).sum()
            ),
            "median_all_input_usd": float(current[INPUT_PRICE].median()),
            "median_continuer_input_usd": float(current.loc[common_index, INPUT_PRICE].median()) if common else np.nan,
            "median_new_input_usd": float(current.loc[sorted(entrants), INPUT_PRICE].median()) if entrants else np.nan,
        })
        previous = current
    return pd.DataFrame(rows)


def forecast_weekly_cost(series, holdout=26, min_history=20):
    """Walk-forward, one-week-ahead Ridge versus last observed price."""
    values = pd.Series(series, dtype=float).sort_index()
    if values.isna().any() or (values < 0).any() or holdout < 1:
        raise ValueError("Expected nonnegative, complete prices and a positive holdout")
    first_test = len(values) - holdout
    if first_test <= max(min_history, 8):
        raise ValueError("Insufficient weeks before the holdout")

    def features(index):
        return [index, values.iloc[index - 1], values.iloc[index - 4], values.iloc[index - 8]]

    rows = []
    for test_index in range(first_test, len(values)):
        train_indices = range(8, test_index)
        x_train = np.asarray([features(index) for index in train_indices], dtype=float)
        y_train = values.iloc[list(train_indices)].to_numpy(dtype=float)
        estimator = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
        estimator.fit(x_train, y_train)
        rows.append({
            "week_start": values.index[test_index],
            "training_end": values.index[test_index - 1],
            "actual": float(values.iloc[test_index]),
            "prediction": float(max(0, estimator.predict([features(test_index)])[0])),
            "baseline": float(values.iloc[test_index - 1]),
        })
    return pd.DataFrame(rows)


def score_forecasts(frame):
    actual = frame["actual"].to_numpy(dtype=float)
    result = {}
    for label, column in (("model", "prediction"), ("baseline", "baseline")):
        predicted = frame[column].to_numpy(dtype=float)
        denominator = np.abs(actual) + np.abs(predicted)
        smape = np.divide(2 * np.abs(actual - predicted), denominator,
                          out=np.zeros_like(actual), where=denominator > 0)
        result[label] = {
            "mae_usd": float(np.mean(np.abs(actual - predicted))),
            "smape_pct": float(100 * np.mean(smape)),
        }
    return result
