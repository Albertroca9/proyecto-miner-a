import unittest

import pandas as pd

from avance.data import prepare_snapshot


class PrepareSnapshotTests(unittest.TestCase):
    def test_keeps_comparable_chat_prices_and_calculates_example_cost(self):
        frame = pd.DataFrame({
            "model_id": ["a", "b", "c", "d"],
            "mode": ["chat", "chat", "embedding", "chat"],
            "input_price_per_1m_tokens": [1.0, 0.0, 1.0, 1.0],
            "output_price_per_1m_tokens": [4.0, 2.0, 2.0, None],
        })
        result = prepare_snapshot(frame)
        self.assertEqual(result.model_id.tolist(), ["a"])
        self.assertEqual(result.iloc[0].example_cost_usd, 2.0)

    def test_rejects_missing_required_columns(self):
        with self.assertRaisesRegex(ValueError, "mode"):
            prepare_snapshot(pd.DataFrame({"model_id": ["a"]}))
