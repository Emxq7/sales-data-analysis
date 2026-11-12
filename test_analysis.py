import tempfile
import unittest
from pathlib import Path
from analysis import load_data, build_summaries


class AnalysisTests(unittest.TestCase):
    def test_load_calculates_revenue(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sales.csv"
            path.write_text(
                "date,order_id,product,quantity,unit_price\n"
                "2026-01-01,1,Book,2,5\n"
            )
            df = load_data(path)
            self.assertEqual(float(df.iloc[0]["revenue"]), 10.0)

    def test_metrics_and_grouping(self):
        import pandas as pd
        df = pd.DataFrame({
            "order_id": [1, 2], "product": ["A", "B"],
            "quantity": [2, 1], "revenue": [10.0, 5.0],
            "month": ["2026-01", "2026-02"]
        })
        products, months, metrics = build_summaries(df)
        self.assertEqual(metrics["total_revenue"], 15.0)
        self.assertEqual(len(products), 2)
        self.assertEqual(len(months), 2)


if __name__ == "__main__":
    unittest.main()
