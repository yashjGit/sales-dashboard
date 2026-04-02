from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "superstore.csv"


def load_data() -> pd.DataFrame:
    """Load and prepare the Superstore dataset."""
    df = pd.read_csv(DATA_PATH, encoding="latin1")

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    df = df.dropna(subset=["Order Date"]).copy()
    df["Month-Year"] = df["Order Date"].dt.strftime("%b-%Y")
    df["Month Sort"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()

    sales_nonzero = df["Sales"].replace(0, np.nan)
    df["Profit Margin %"] = ((df["Profit"] / sales_nonzero) * 100).fillna(0)

    return df.sort_values("Order Date").reset_index(drop=True)
