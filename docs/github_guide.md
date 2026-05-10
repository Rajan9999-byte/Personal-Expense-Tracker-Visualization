# 🐙 GitHub Upload Guide

## Best Repository Name
`Personal-Expense-Tracker-Visualization`

## Description
"A Python project to track, analyse & visualise personal expenses using Pandas, Matplotlib, Seaborn, Plotly & Streamlit. Includes interactive dashboard, 7 charts, and auto-generated reports."

## GitHub Topics / Tags
`python` `pandas` `data-visualization` `streamlit` `plotly` `expense-tracker` `personal-finance` `matplotlib` `seaborn` `data-analysis` `portfolio-project`

---

## Step-by-Step Upload

### 1. Create Repository on GitHub
- Go to github.com → New Repository
- Name: `Personal-Expense-Tracker-Visualization`
- Visibility: Public
- Do NOT initialise with README (you already have one)
- Click "Create repository"

### 2. Initialise Git Locally
```bash
cd Personal-Expense-Tracker-Visualization
git init
git add .
git commit -m "feat: initial project setup with full pipeline and dashboard"
```

### 3. Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/Personal-Expense-Tracker-Visualization.git
git branch -M main
git push -u origin main
```

---

## Day-wise Commit Strategy

```bash
# Day 1 – Setup
git add requirements.txt .gitignore README.md
git commit -m "feat: initialise project structure and requirements"

# Day 2 – Data
git add src/generate_data.py data/expenses.csv
git commit -m "feat: add synthetic 6-month expense data generator"

# Day 3 – Analysis
git add src/analysis.py
git commit -m "feat: add data cleaning and category/monthly/payment aggregation"

# Day 4 – Charts
git add src/visualizations.py outputs/
git commit -m "feat: add 7 matplotlib/seaborn charts to outputs/"

# Day 5 – Dashboard
git add dashboard.py
git commit -m "feat: add interactive Streamlit dashboard with Plotly and filters"

# Day 6 – Reports + Docs
git add src/report.py reports/ docs/ main.py
git commit -m "docs: add report generator, interview prep, and GitHub upload guide"
```

---

## Screenshots to Capture for GitHub

1. `images/01_folder_structure.png` — VS Code Explorer panel
2. `images/02_dataset_preview.png` — Terminal showing first 10 rows
3. `images/03_terminal_output.png` — Full pipeline output
4. `images/04_dashboard_overview.png` — Dashboard landing page
5. `images/05_category_tab.png` — Categories tab
6. `images/06_monthly_tab.png` — Monthly trends tab
7. `images/07_payment_tab.png` — Payment analysis tab
8. `images/08_report_tab.png` — Report tab with insights

Upload these to the `images/` folder and reference them in README.md.

---

## Deploy on Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to share.streamlit.io
3. Connect your GitHub account
4. Select repo: `Personal-Expense-Tracker-Visualization`
5. Main file: `dashboard.py`
6. Click Deploy

Your dashboard will be live at:
`https://YOUR_USERNAME-personal-expense-tracker.streamlit.app`

Add this URL to your LinkedIn profile and resume!
