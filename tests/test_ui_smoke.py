from __future__ import annotations

import unittest

from streamlit.testing.v1 import AppTest


class StreamlitUiSmokeTests(unittest.TestCase):
    def test_sample_analysis_renders_all_navigation_tabs(self) -> None:
        app = AppTest.from_file("app.py", default_timeout=15)
        app.run()
        self.assertEqual(len(app.exception), 0)

        self.assertGreaterEqual(len(app.selectbox), 1)
        app.selectbox[0].set_value("multi_asset_portfolio.csv")
        app.run()
        self.assertEqual(len(app.exception), 0)

        nav_labels = [
            "OV  Overview",
            "DP  Data Profile",
            "RT  Return Analysis",
            "RK  Risk Analysis",
            "DV  Diversification",
            "IN  Insights",
            "RL  Applied Rules",
            "RP  Reports",
        ]
        self.assertGreaterEqual(len(app.radio), 1)
        for label in nav_labels:
            app.radio[0].set_value(label)
            app.run()
            self.assertEqual(len(app.exception), 0, msg=f"{label} rendered with exception(s)")


if __name__ == "__main__":
    unittest.main()
