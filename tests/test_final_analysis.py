import unittest

import numpy as np
import pandas as pd

from avance.data import INPUT_PRICE, OUTPUT_PRICE
from avance.final_analysis import catalog_dynamics, forecast_weekly_cost, score_forecasts


class CatalogDynamicsTests(unittest.TestCase):
    def test_counts_entrants_continuers_exits_and_price_changes(self):
        frame = pd.DataFrame({
            "week_start": pd.to_datetime([
                "2026-01-05", "2026-01-05", "2026-01-12", "2026-01-12"
            ]),
            "model_id": ["a", "b", "a", "c"],
            INPUT_PRICE: [2.0, 4.0, 1.0, 8.0],
            OUTPUT_PRICE: [4.0, 8.0, 4.0, 8.0],
        })
        result = catalog_dynamics(frame)
        second = result.iloc[1]
        self.assertEqual((second.n_listings, second.entrants, second.continuers, second.exits), (2, 1, 1, 1))
        self.assertEqual(second.input_price_changes, 1)
        self.assertEqual(second.median_continuer_input_usd, 1.0)
        self.assertEqual(second.median_new_input_usd, 8.0)


class ForecastTests(unittest.TestCase):
    def test_holdout_uses_only_prior_weeks_and_persistence_baseline(self):
        dates = pd.date_range("2026-01-05", periods=16, freq="W-MON")
        series = pd.Series(np.arange(1.0, 17.0), index=dates)
        result = forecast_weekly_cost(series, holdout=3, min_history=8)
        self.assertEqual(result.week_start.tolist(), list(dates[-3:]))
        self.assertEqual(result.training_end.tolist(), list(dates[-4:-1]))
        self.assertEqual(result.baseline.tolist(), [13.0, 14.0, 15.0])
        self.assertEqual(result.actual.tolist(), [14.0, 15.0, 16.0])

    def test_score_forecasts_handles_zero_without_division_error(self):
        frame = pd.DataFrame({"actual": [0.0, 2.0], "baseline": [0.0, 1.0], "prediction": [0.0, 3.0]})
        scores = score_forecasts(frame)
        self.assertEqual(scores["baseline"]["mae_usd"], 0.5)
        self.assertTrue(np.isfinite(scores["model"]["smape_pct"]))


if __name__ == "__main__":
    unittest.main()
