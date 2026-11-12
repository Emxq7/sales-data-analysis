"""Analyze synthetic retail transactions and export business summaries."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "sales.csv"
OUTPUT = ROOT / "output"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"date", "order_id", "product", "quantity", "unit_price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for column in ("quantity", "unit_price"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=list(required)).copy()
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def build_summaries(df: pd.DataFrame):
    by_product = (df.groupby("product", as_index=False)["revenue"]
                    .sum().sort_values("revenue", ascending=False))
    by_month = (df.groupby("month", as_index=False)["revenue"]
                  .sum().sort_values("month"))
    metrics = {
        "transactions": int(df["order_id"].nunique()),
        "units_sold": int(df["quantity"].sum()),
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "average_transaction_value": round(float(df.groupby("order_id")["revenue"].sum().mean()), 2),
        "products_sold": int(df["product"].nunique()),
    }
    return by_product, by_month, metrics


def save_chart(by_month: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(by_month["month"], by_month["revenue"], marker="o")
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def run_analysis(data_path: Path, output_dir: Path):
    df = load_data(data_path)
    product, month, metrics = build_summaries(df)
    output_dir.mkdir(parents=True, exist_ok=True)
    product.to_csv(output_dir / "revenue_by_product.csv", index=False)
    month.to_csv(output_dir / "revenue_by_month.csv", index=False)
    pd.DataFrame([metrics]).to_csv(output_dir / "key_metrics.csv", index=False)
    save_chart(month, output_dir / "monthly_revenue.png")
    return metrics


if __name__ == "__main__":
    results = run_analysis(DATA_PATH, OUTPUT)
    print("Analysis complete")
    for name, value in results.items():
        print(f"{name.replace('_', ' ').title()}: {value}")
    print(f"Reports saved to {OUTPUT}")
