import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class FinalDemoTests(unittest.TestCase):
    def test_final_demo_shows_recommender_and_evaluation_without_errors(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "streamlit_app.py"), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([tab.label for tab in app.tabs], ["Recomendador", "Evolución", "Evaluación"])
        self.assertGreaterEqual(len(app.dataframe), 1)
        app.number_input[2].set_value(128_000).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.number_input[2].value, 128_000)


if __name__ == "__main__":
    unittest.main()
