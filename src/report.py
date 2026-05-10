"""
report.py
---------
Generates a plain-text summary report and saves CSVs of key analyses.
"""

import os
import pandas as pd
from datetime import datetime
from analysis import (load_and_clean, category_summary, monthly_summary,
                      payment_method_summary, top_expenses, key_metrics)

os.makedirs("reports", exist_ok=True)


def generate_text_report(df: pd.DataFrame) -> str:
    metrics = key_metrics(df)
    cat     = category_summary(df)
    mon     = monthly_summary(df)
    pay     = payment_method_summary(df)
    top     = top_expenses(df, 5)

    lines = []
    def h(title):  lines.append(f"\n{'='*60}\n  {title}\n{'='*60}")
    def row(k, v): lines.append(f"  {k:<30}: {v}")

    lines.append("=" * 60)
    lines.append("  PERSONAL EXPENSE TRACKER — FULL REPORT")
    lines.append(f"  Generated on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    lines.append("=" * 60)

    h("📊 KEY METRICS")
    row("Total Spent",           f"₹{metrics['total_spent']:,.2f}")
    row("Total Transactions",    metrics["total_transactions"])
    row("Date Range (days)",     metrics["date_range_days"])
    row("Months Covered",        metrics["months_covered"])
    row("Avg Daily Spending",    f"₹{metrics['avg_daily_spending']:,.2f}")
    row("Avg Per Transaction",   f"₹{metrics['avg_transaction']:,.2f}")
    row("Highest Spend Category",metrics["highest_category"])
    row("Largest Single Expense",f"₹{metrics['highest_single']:,.2f}")
    row("Most Used Payment",     metrics["most_used_payment"])

    h("📂 CATEGORY-WISE BREAKDOWN")
    for _, r in cat.iterrows():
        lines.append(f"  {r['category']:<20} ₹{r['total_amount']:>10,.2f}  ({r['percentage']:>5.1f}%)")

    h("📅 MONTHLY SPENDING")
    for _, r in mon.iterrows():
        lines.append(f"  {r['month_name']:<12} ₹{r['total']:>10,.2f}  ({r['transactions']} txns)")

    h("💳 PAYMENT METHOD BREAKDOWN")
    for _, r in pay.iterrows():
        lines.append(f"  {r['payment_method']:<15} ₹{r['total_amount']:>10,.2f}  ({r['percentage']:>5.1f}%)")

    h("🔝 TOP 5 LARGEST EXPENSES")
    for _, r in top.iterrows():
        lines.append(f"  {str(r['date'].date()):<12} {r['category']:<20} ₹{r['amount']:>8,.2f}  {r['note']}")

    h("💡 INSIGHTS & RECOMMENDATIONS")
    top_cat = cat.iloc[0]
    lines.append(f"  • Your highest spending category is '{top_cat['category']}' "
                 f"({top_cat['percentage']}% of total). Consider setting a monthly cap.")
    avg_daily = metrics["avg_daily_spending"]
    if avg_daily > 1500:
        lines.append(f"  • Avg daily spend (₹{avg_daily:,.2f}) is high. Try the 50-30-20 budget rule.")
    else:
        lines.append(f"  • Avg daily spend (₹{avg_daily:,.2f}) looks manageable. Keep tracking!")
    lines.append(f"  • You used '{metrics['most_used_payment']}' most often. "
                 f"Using credit cards can offer cashback rewards.")
    lines.append(f"  • Review your top expenses monthly to identify non-essential spending.")
    lines.append("\n" + "=" * 60)

    return "\n".join(lines)


def save_all(df: pd.DataFrame):
    # Text report
    report_text = generate_text_report(df)
    with open("reports/expense_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    print("✅ reports/expense_report.txt")

    # CSV summaries
    category_summary(df).to_csv("reports/category_summary.csv", index=False)
    print("✅ reports/category_summary.csv")

    monthly_summary(df).to_csv("reports/monthly_summary.csv", index=False)
    print("✅ reports/monthly_summary.csv")

    payment_method_summary(df).to_csv("reports/payment_summary.csv", index=False)
    print("✅ reports/payment_summary.csv")

    top_expenses(df, 10).to_csv("reports/top_expenses.csv", index=False)
    print("✅ reports/top_expenses.csv")

    print(report_text)
    return report_text


if __name__ == "__main__":
    df = load_and_clean()
    save_all(df)
