# 💼 Interview Preparation Guide
## Personal Expense Tracker with Data Visualization

---

## Q1. Explain your project.

**HR Answer:**
"I built a Personal Expense Tracker using Python that helps individuals understand their spending habits through data visualization. The tool tracks expenses across categories like Food, Rent, Shopping, and Entertainment, then generates charts and reports to show where the money goes. I also built an interactive web dashboard using Streamlit where users can filter by month, category, or payment method and download reports."

**Technical Answer:**
"The project has four main modules:
1. `generate_data.py` — creates a synthetic 6-month dataset with 10 expense categories and 5 payment methods using Pandas and random/datetime.
2. `analysis.py` — loads and cleans the CSV, then applies groupby aggregations for category summaries, monthly trends, and payment analysis.
3. `visualizations.py` — generates 7 charts using Matplotlib and Seaborn — bar, line, pie, donut, and stacked bar charts.
4. `dashboard.py` — a Streamlit app with Plotly interactive charts, sidebar filters, budget tracking, a transaction search log, and report download."

---

## Q2. Why did you choose Python for this project?

**Answer:**
"Python has the best ecosystem for data work. Pandas makes CSV loading and groupby operations 10× faster to write than raw Python. Matplotlib and Plotly cover both static and interactive charts. Streamlit lets you build a full web dashboard without any JavaScript. It's also the dominant language in data analysis and finance, making this project directly relevant to industry roles."

---

## Q3. How did you clean the data?

**Technical Answer:**
"I applied four cleaning steps in `analysis.py`:
1. `pd.to_datetime()` with `errors='coerce'` to parse dates and nullify invalid ones.
2. `dropna()` on critical columns: date, amount, and category.
3. `drop_duplicates()` to remove exact duplicate rows.
4. `pd.to_numeric(errors='coerce')` and filtering `amount > 0` to ensure valid positive numbers.
After cleaning, I added derived columns: `month`, `month_name`, `day_of_week`, and `week` for aggregation."

---

## Q4. How did you perform category-wise analysis?

**Technical Answer:**
"Using Pandas `groupby`:
```python
grp = df.groupby('category')['amount'].sum().reset_index()
grp['percentage'] = grp['total_amount'] / grp['total_amount'].sum() * 100
grp['avg_per_transaction'] = df.groupby('category')['amount'].mean().values
```
This gives total spend, share percentage, and average transaction size per category — the three most useful business metrics."

---

## Q5. How did you build the dashboard?

**Technical Answer:**
"I used Streamlit as the framework and Plotly for interactive charts. The dashboard has:
- Sidebar with multiselect filters (month, category, payment method) that filter the underlying DataFrame in real time.
- KPI metric cards showing total spend, transactions, daily average, and top category.
- A budget progress bar comparing avg monthly spend against a user-defined budget.
- Six tabs: Categories, Monthly Trends, Payment Analysis, Daily Patterns, Transaction Log, and Report.
- Download buttons for filtered CSV and the text report."

---

## Q6. What is a rolling average and why did you use it?

**Answer:**
"A rolling average smooths out day-to-day noise in data. For example, if you spend ₹5,000 on one day for a shopping trip, it spikes the daily chart. A 7-day rolling average shows the underlying trend instead of the spike.
In Pandas: `df['7d_rolling'] = df['daily_total'].rolling(7, min_periods=1).mean()`
This is widely used in financial time series, stock prices, and web analytics."

---

## Q7. How did you structure your code? Why?

**Answer:**
"I used a modular structure — separate Python files for each concern:
- `generate_data.py` — data creation only
- `analysis.py` — pure data logic, no UI
- `visualizations.py` — chart generation only
- `report.py` — report formatting
- `dashboard.py` — UI layer only

This follows the Single Responsibility Principle. It means I can update chart styles without touching analysis code, or swap the data source without changing the dashboard. In a team project, different developers can work on separate modules."

---

## Q8. How would you add a real bank account connection to this project?

**Answer:**
"For a production version, I'd connect to a bank API or data aggregator like Plaid, Razorpay, or a bank's open banking API. The API returns transaction JSON, which I'd parse into the same CSV schema the project already uses. The entire analysis and dashboard pipeline would work unchanged — only the data source changes. This is exactly why I separated data generation from analysis."

---

## Q9. What Python libraries did you use and why?

| Library | Why Used |
|---------|---------|
| **Pandas** | DataFrame operations, groupby, pivot_table |
| **NumPy** | Numerical computations, random seed |
| **Matplotlib** | Static chart generation and saving |
| **Seaborn** | Styled statistical charts with themes |
| **Plotly** | Interactive charts in the dashboard |
| **Streamlit** | Web dashboard without JavaScript |
| **datetime** | Date parsing and time period extraction |

---

## Q10. What was the most challenging part of this project?

**Answer:**
"The most challenging part was designing the dashboard filter logic. When a user selects months or categories in the sidebar, every chart, KPI metric, and table needs to update from the same filtered DataFrame. I solved this by applying all filters once at the top of `dashboard.py` to create a single `df` variable, and passing it to every analysis function. This ensures all panels are always in sync and there's a single source of truth."

---

## Bonus: HR Behavioural Questions

**"Why did you build this project?"**
"As a student, I wanted a project that's relevant to both Data Analysis and Finance roles. Expense tracking is a universal problem everyone can relate to, which also makes it easy to explain in interviews."

**"What would you improve next?"**
"I'd add: (1) a machine learning model to predict next month's spending based on trends, (2) email alerts when spending exceeds budget, (3) CSV import from real bank statement exports, and (4) multi-user support with login authentication."

**"Is this project deployed anywhere?"**
"The Streamlit app can be deployed for free on Streamlit Cloud in under 5 minutes by connecting the GitHub repo. This makes it publicly accessible as a live demo link to include in my resume."
