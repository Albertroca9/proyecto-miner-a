import unittest

import numpy as np
import pandas as pd

from avance.models import CLASSIFICATION_FEATURES, make_group_split, price_bands


class ModelDesignTests(unittest.TestCase):
    def test_classification_features_do_not_include_prices_or_ids(self):
        self.assertFalse(any("price" in name or name in {"model_id", "model_name"} for name in CLASSIFICATION_FEATURES))

    def test_group_split_keeps_model_names_separate(self):
        frame = pd.DataFrame({"model_name": ["a", "a", "b", "b", "c", "c", "d", "d"]})
        train, test = make_group_split(frame, test_size=0.25, random_state=7)
        self.assertFalse(set(frame.iloc[train].model_name) & set(frame.iloc[test].model_name))

    def test_price_band_thresholds_come_only_from_training_prices(self):
        train = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        test = np.array([1000.0])
        train_labels, test_labels, thresholds = price_bands(train, test)
        self.assertLess(thresholds[1], 6.0)
        self.assertEqual(test_labels.tolist(), [2])
        self.assertEqual(len(train_labels), 6)
