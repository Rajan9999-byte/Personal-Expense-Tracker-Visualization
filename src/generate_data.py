"""
generate_data.py
----------------
Generates a synthetic 6-month personal expense dataset and saves it to data/expenses.csv
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ── Seed for reproducibility ──────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

# ── Categories with realistic spending ranges (INR) ───────────────────────────
CATEGORIES = {
    "Food & Dining":      (150, 800),
    "Transportation":     (50,  500),
    "Shopping":           (300, 3000),
    "Entertainment":      (100, 1500),
    "Utilities":          (500, 2500),
    "Healthcare":         (200, 2000),
    "Education":          (500, 5000),
    "Rent":               (8000, 8000),
    "Groceries":          (200, 1200),
    "Personal Care":      (100, 800),
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

NOTES = {
    "Food & Dining":    ["Zomato order", "Restaurant dinner", "Cafe coffee", "Street food", "Lunch with friends"],
    "Transportation":   ["Uber ride", "Auto fare", "Metro card recharge", "Petrol", "Bus ticket"],
    "Shopping":         ["Amazon purchase", "Clothes", "Electronics", "Books", "Home decor"],
    "Entertainment":    ["Movie tickets", "Netflix subscription", "Concert", "Gaming", "OTT subscription"],
    "Utilities":        ["Electricity bill", "Internet bill", "Water bill", "Gas bill", "Mobile recharge"],
    "Healthcare":       ["Doctor visit", "Medicines", "Lab tests", "Gym membership", "Vitamins"],
    "Education":        ["Online course", "Books", "Coaching fees", "Stationery", "Software subscription"],
    "Rent":             ["Monthly rent"],
    "Groceries":        ["BigBasket order", "Local market", "Vegetables", "Fruits", "Dairy products"],
    "Personal Care":    ["Haircut", "Skincare products", "Salon visit", "Grooming kit", "Perfume"],
}


def generate_expenses(start_date: str = "2024-07-01", months: int = 6, n_per_day: tuple = (1, 5)) -> pd.DataFrame:
    """Return a DataFrame of synthetic expense records."""
    records = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = current + timedelta(days=30 * months)

    while current < end:
        # Rent is added on the 1st of each month
        if current.day == 1:
            records.append({
                "date": current.strftime("%Y-%m-%d"),
                "category": "Rent",
                "amount": 8000,
                "payment_method": "Net Banking",
                "note": "Monthly rent",
            })

        n = random.randint(*n_per_day)
        for _ in range(n):
            cat = random.choice([c for c in CATEGORIES if c != "Rent"])
            low, high = CATEGORIES[cat]
            amount = round(random.uniform(low, high), 2)
            records.append({
                "date": current.strftime("%Y-%m-%d"),
                "category": cat,
                "amount": amount,
                "payment_method": random.choice(PAYMENT_METHODS),
                "note": random.choice(NOTES[cat]),
            })
        current += timedelta(days=1)

    return pd.DataFrame(records)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_expenses()
    df.to_csv("data/expenses.csv", index=False)
    print(f"✅ Generated {len(df)} expense records → data/expenses.csv")
    print(df.head(10).to_string(index=False))
