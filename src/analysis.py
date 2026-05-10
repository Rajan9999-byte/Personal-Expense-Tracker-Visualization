"""
analysis.py
-----------
Loads, cleans, and analyses the expense CSV.
Returns clean DataFrames and summary statistics used by both
the CLI report and the Streamlit dashboard.
"""

import pandas as pd
import numpy as np
import os


# ── Load & Clean ──────────────────────────────────────────────────────────────

def load_and_clean(filepath: str = "data/expenses.csv") -> pd.DataFrame:
    """Load CSV, parse dates, remove duplicates and nulls, add helper columns."""
    df = pd.read_csv(filepath)

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date", "amount", "category"], inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Ensure amount is numeric and positive
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]

    # Helper columns
    df["month"] = df["date"].dt.to_period("M").astype(str)          # "2024-07"
    df["month_name"] = df["date"].dt.strftime("%b %Y")              # "Jul 2024"
    df["day_of_week"] = df["date"].dt.day_name()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    # Sort chronologically
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


# ── Aggregations ──────────────────────────────────────────────────────────────

def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Total and percentage spend per category."""
    grp = df.groupby("category")["amount"].sum().reset_index()
    grp.columns = ["category", "total_amount"]
    grp["percentage"] = (grp["total_amount"] / grp["total_amount"].sum() * 100).round(2)
    grp["avg_per_transaction"] = df.groupby("category")["amount"].mean().values
    grp.sort_values("total_amount", ascending=False, inplace=True)
    grp.reset_index(drop=True, inplace=True)
    return grp


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Total spend per calendar month."""
    grp = df.groupby(["month", "month_name"])["amount"].agg(
        total="sum", transactions="count", avg_per_day="mean"
    ).reset_index()
    grp.sort_values("month", inplace=True)
    grp.reset_index(drop=True, inplace=True)
    return grp


def payment_method_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Spend breakdown by payment method."""
    grp = df.groupby("payment_method")["amount"].sum().reset_index()
    grp.columns = ["payment_method", "total_amount"]
    grp["percentage"] = (grp["total_amount"] / grp["total_amount"].sum() * 100).round(2)
    grp.sort_values("total_amount", ascending=False, inplace=True)
    return grp


def daily_spending(df: pd.DataFrame) -> pd.DataFrame:
    """Sum of expenses per day."""
    grp = df.groupby("date")["amount"].sum().reset_index()
    grp.columns = ["date", "daily_total"]
    grp["7d_rolling"] = grp["daily_total"].rolling(7, min_periods=1).mean()
    return grp


def top_expenses(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top-N individual transactions by amount."""
    return df.nlargest(n, "amount")[["date", "category", "amount", "payment_method", "note"]].reset_index(drop=True)


def weekday_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Average spend per day of week."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grp = df.groupby("day_of_week")["amount"].mean().reindex(order).reset_index()
    grp.columns = ["day_of_week", "avg_amount"]
    return grp


# ── Key Metrics ───────────────────────────────────────────────────────────────

def key_metrics(df: pd.DataFrame) -> dict:
    total = df["amount"].sum()
    days  = (df["date"].max() - df["date"].min()).days + 1
    return {
        "total_spent":           round(total, 2),
        "total_transactions":    len(df),
        "avg_daily_spending":    round(total / days, 2),
        "avg_transaction":       round(df["amount"].mean(), 2),
        "highest_category":      df.groupby("category")["amount"].sum().idxmax(),
        "highest_single":        round(df["amount"].max(), 2),
        "most_used_payment":     df["payment_method"].mode()[0],
        "date_range_days":       days,
        "months_covered":        df["month"].nunique(),
    }


if __name__ == "__main__":
    df = load_and_clean()
    metrics = key_metrics(df)
    print("\n📊 KEY METRICS")
    for k, v in metrics.items():
        print(f"  {k:<25}: {v}")
    print("\n📂 CATEGORY SUMMARY")
    print(category_summary(df).to_string(index=False))
