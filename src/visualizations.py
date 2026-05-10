"""
visualizations.py
-----------------
All chart-generation functions.
Each function saves a PNG to outputs/ and returns the matplotlib Figure
so Streamlit can also render them inline.
"""

import os
import matplotlib
matplotlib.use("Agg")           # non-interactive backend safe for scripts & Streamlit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

# ── Shared Style ──────────────────────────────────────────────────────────────
PALETTE   = "husl"
BG        = "#F8F9FA"
ACCENT    = "#4361EE"
FONT_MAIN = "DejaVu Sans"

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "font.family":       FONT_MAIN,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

os.makedirs("outputs", exist_ok=True)


def _save(fig: plt.Figure, name: str) -> str:
    path = f"outputs/{name}"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    return path


# ── 1. Category Bar Chart ─────────────────────────────────────────────────────
def plot_category_bar(cat_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette(PALETTE, len(cat_df))
    bars = ax.barh(cat_df["category"], cat_df["total_amount"], color=colors, edgecolor="white", linewidth=0.6)

    for bar, val in zip(bars, cat_df["total_amount"]):
        ax.text(bar.get_width() + 80, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", fontsize=9, color="#333")

    ax.set_xlabel("Total Amount Spent (₹)", fontsize=11)
    ax.set_title("💰 Category-wise Total Spending", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.invert_yaxis()
    fig.tight_layout()
    _save(fig, "01_category_bar.png")
    return fig


# ── 2. Monthly Trend Line Chart ───────────────────────────────────────────────
def plot_monthly_trend(monthly_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly_df["month_name"], monthly_df["total"], marker="o",
            color=ACCENT, linewidth=2.5, markersize=8, markerfacecolor="white",
            markeredgewidth=2, markeredgecolor=ACCENT)

    for i, row in monthly_df.iterrows():
        ax.annotate(f"₹{row['total']:,.0f}",
                    (row["month_name"], row["total"]),
                    textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=9, color="#333")

    ax.fill_between(monthly_df["month_name"], monthly_df["total"],
                    alpha=0.12, color=ACCENT)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Total Spending (₹)", fontsize=11)
    ax.set_title("📈 Monthly Spending Trend", fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    _save(fig, "02_monthly_trend.png")
    return fig


# ── 3. Payment Method Pie Chart ───────────────────────────────────────────────
def plot_payment_pie(pay_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 8))
    explode = [0.04] * len(pay_df)
    wedges, texts, autotexts = ax.pie(
        pay_df["total_amount"],
        labels=pay_df["payment_method"],
        autopct="%1.1f%%",
        explode=explode,
        colors=sns.color_palette(PALETTE, len(pay_df)),
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax.set_title("💳 Payment Method Distribution", fontsize=14, fontweight="bold", pad=20)
    fig.tight_layout()
    _save(fig, "03_payment_pie.png")
    return fig


# ── 4. Daily Spending Trend ───────────────────────────────────────────────────
def plot_daily_trend(daily_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(daily_df["date"], daily_df["daily_total"],
           color=ACCENT, alpha=0.4, width=0.8, label="Daily Spend")
    ax.plot(daily_df["date"], daily_df["7d_rolling"],
            color="#E63946", linewidth=2, label="7-Day Rolling Avg")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Amount (₹)", fontsize=11)
    ax.set_title("📅 Daily Spending with 7-Day Rolling Average", fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend(fontsize=10)
    fig.autofmt_xdate(rotation=30)
    fig.tight_layout()
    _save(fig, "04_daily_trend.png")
    return fig


# ── 5. Weekday Heatmap-Bar ────────────────────────────────────────────────────
def plot_weekday_bar(weekday_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [ACCENT if v == weekday_df["avg_amount"].max() else "#ADB5BD"
              for v in weekday_df["avg_amount"]]
    bars = ax.bar(weekday_df["day_of_week"], weekday_df["avg_amount"],
                  color=colors, edgecolor="white", linewidth=0.6)
    for bar, val in zip(bars, weekday_df["avg_amount"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"₹{val:,.0f}", ha="center", fontsize=9, color="#333")
    ax.set_xlabel("Day of Week", fontsize=11)
    ax.set_ylabel("Avg Spend (₹)", fontsize=11)
    ax.set_title("📆 Average Spending by Day of Week", fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "05_weekday_bar.png")
    return fig


# ── 6. Category % Donut ───────────────────────────────────────────────────────
def plot_category_donut(cat_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 9))
    colors = sns.color_palette(PALETTE, len(cat_df))
    wedges, texts, autotexts = ax.pie(
        cat_df["total_amount"],
        labels=cat_df["category"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        pctdistance=0.82,
        wedgeprops={"width": 0.5, "edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.set_title("🍩 Category Share of Total Spending", fontsize=14, fontweight="bold", pad=20)
    fig.tight_layout()
    _save(fig, "06_category_donut.png")
    return fig


# ── 7. Monthly Category Stacked Bar ──────────────────────────────────────────
def plot_monthly_category_stack(df: pd.DataFrame) -> plt.Figure:
    pivot = df.pivot_table(index="month_name", columns="category",
                           values="amount", aggfunc="sum").fillna(0)
    # keep month order
    month_order = df.drop_duplicates("month_name").sort_values("month")["month_name"].tolist()
    pivot = pivot.reindex(month_order)

    fig, ax = plt.subplots(figsize=(13, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax,
               color=sns.color_palette(PALETTE, pivot.shape[1]),
               edgecolor="white", linewidth=0.4)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Total Spending (₹)", fontsize=11)
    ax.set_title("📊 Monthly Spending by Category (Stacked)", fontsize=14, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.tick_params(axis="x", rotation=30)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)
    fig.tight_layout()
    _save(fig, "07_monthly_category_stack.png")
    return fig


if __name__ == "__main__":
    from analysis import load_and_clean, category_summary, monthly_summary, payment_method_summary, daily_spending, weekday_summary
    df  = load_and_clean()
    cat = category_summary(df)
    mon = monthly_summary(df)
    pay = payment_method_summary(df)
    dai = daily_spending(df)
    wkd = weekday_summary(df)

    plot_category_bar(cat);         print("✅ 01_category_bar.png")
    plot_monthly_trend(mon);        print("✅ 02_monthly_trend.png")
    plot_payment_pie(pay);          print("✅ 03_payment_pie.png")
    plot_daily_trend(dai);          print("✅ 04_daily_trend.png")
    plot_weekday_bar(wkd);          print("✅ 05_weekday_bar.png")
    plot_category_donut(cat);       print("✅ 06_category_donut.png")
    plot_monthly_category_stack(df);print("✅ 07_monthly_category_stack.png")
    print("\nAll charts saved to outputs/")
