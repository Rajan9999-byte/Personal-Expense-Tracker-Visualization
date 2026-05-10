"""
main.py
-------
Command-line runner — generates data, runs analysis, creates all charts, and produces reports.
Run:  python main.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.generate_data import generate_expenses
from src.analysis import (
    load_and_clean, category_summary, monthly_summary,
    payment_method_summary, daily_spending, weekday_summary, key_metrics,
)
from src.visualizations import (
    plot_category_bar, plot_monthly_trend, plot_payment_pie,
    plot_daily_trend, plot_weekday_bar, plot_category_donut,
    plot_monthly_category_stack,
)
from src.report import save_all
import matplotlib.pyplot as plt


def run():
    print("\n" + "=" * 60)
    print("  💰 PERSONAL EXPENSE TRACKER — RUNNING PIPELINE")
    print("=" * 60)

    # ── Step 1: Generate data ─────────────────────────────────
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/expenses.csv"):
        print("\n📝 Generating synthetic expense data…")
        df_raw = generate_expenses()
        df_raw.to_csv("data/expenses.csv", index=False)
        print(f"   → {len(df_raw)} records saved to data/expenses.csv")
    else:
        print("\n📂 Loading existing data/expenses.csv")

    # ── Step 2: Load & Clean ──────────────────────────────────
    print("\n🔧 Cleaning and transforming data…")
    df = load_and_clean("data/expenses.csv")
    print(f"   → {len(df)} clean records | {df['month'].nunique()} months")

    # ── Step 3: Key Metrics ───────────────────────────────────
    print("\n📊 KEY METRICS")
    metrics = key_metrics(df)
    for k, v in metrics.items():
        print(f"   {k:<28}: {v}")

    # ── Step 4: Charts ────────────────────────────────────────
    print("\n🎨 Generating visualizations…")
    os.makedirs("outputs", exist_ok=True)

    cat = category_summary(df)
    mon = monthly_summary(df)
    pay = payment_method_summary(df)
    dai = daily_spending(df)
    wkd = weekday_summary(df)

    plot_category_bar(cat);             print("   ✅ 01_category_bar.png")
    plot_monthly_trend(mon);            print("   ✅ 02_monthly_trend.png")
    plot_payment_pie(pay);              print("   ✅ 03_payment_pie.png")
    plot_daily_trend(dai);              print("   ✅ 04_daily_trend.png")
    plot_weekday_bar(wkd);              print("   ✅ 05_weekday_bar.png")
    plot_category_donut(cat);           print("   ✅ 06_category_donut.png")
    plot_monthly_category_stack(df);    print("   ✅ 07_monthly_category_stack.png")

    plt.close("all")

    # ── Step 5: Report ────────────────────────────────────────
    print("\n📄 Generating reports…")
    save_all(df)

    print("\n" + "=" * 60)
    print("  ✅ PIPELINE COMPLETE")
    print("  📁 Charts  → outputs/")
    print("  📁 Reports → reports/")
    print("=" * 60)
    print("\n💡 To launch the interactive dashboard:")
    print("   streamlit run dashboard.py\n")


if __name__ == "__main__":
    run()
