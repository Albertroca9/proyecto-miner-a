import unittest

import pandas as pd

from avance.history import prepare_history, price_changes, weekly_summary


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame({
            "week_start": ["2026-01-05", "2026-01-12", "2026-01-05", "2026-01-12", "2026-01-12"],
            "model_id": ["a", "a", "b", "b", "c"],
            "mode": ["chat"] * 5,
            "input_price_per_1m_tokens": [2.0, 1.0, 4.0, 4.0, 0.0],
            "output_price_per_1m_tokens": [4.0, 3.0, 8.0, 8.0, 1.0],
        })

    def test_weekly_summary_uses_eligible_rows_only(self):
        result = weekly_summary(prepare_history(self.frame))
        self.assertEqual(result.n_listings.tolist(), [2, 2])
        self.assertEqual(result.median_input_usd.tolist(), [3.0, 2.5])

    def test_price_changes_match_same_model_across_weeks(self):
        result = price_changes(prepare_history(self.frame), "input_price_per_1m_tokens")
        self.assertEqual(result, {"comparisons": 2, "changes": 1, "decreases": 1, "increases": 0, "models_changed": 1})
