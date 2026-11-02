import unittest

import pandas as pd

from avance.recommend import recommend


class RecommendTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame({
            "model_id": ["cheap_short", "vision", "text"],
            "model_name": ["A", "B", "C"],
            "provider": ["p1", "p2", "p3"],
            "max_input_tokens": [1000, 8000, 8000],
            "supports_vision": [False, True, False],
            "input_price_per_1m_tokens": [0.1, 0.5, 0.3],
            "output_price_per_1m_tokens": [0.2, 1.0, 0.5],
        })

    def test_filters_requirements_and_orders_by_workload_cost(self):
        result = recommend(self.frame, 1_000_000, 250_000, 4000, ["supports_vision"])
        self.assertEqual(result.model_id.tolist(), ["vision"])
        self.assertAlmostEqual(result.iloc[0].estimated_cost_usd, 0.75)

    def test_rejects_negative_volume(self):
        with self.assertRaises(ValueError):
            recommend(self.frame, -1, 0, 0, [])

    def test_without_capability_returns_cheapest_eligible_model(self):
        result = recommend(self.frame, 1_000_000, 250_000, 4000, [])
        self.assertEqual(result.model_id.tolist(), ["text", "vision"])
