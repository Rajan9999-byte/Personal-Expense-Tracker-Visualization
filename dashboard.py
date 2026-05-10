"""
dashboard.py  ──  Streamlit Personal Expense Tracker Dashboard
--------------------------------------------------------------
Run:  streamlit run dashboard.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from src.generate_data import generate_expenses
from src.analysis import (
    load_and_clean, category_summary, monthly_summary,
    payment_method_summary, daily_spending, top_expenses,
    weekday_summary, key_metrics,
)
from src.report import generate_text_report

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💰 Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F0F2F6; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 4px solid #4361EE;
    }
    div[data-testid="metric-container"] label {
        font-size: 13px !important;
        color: #6C757D !important;
        font-weight: 600 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #212529 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #1E1E2E; }
    section[data-testid="stSidebar"] * { color: #CDD6F4 !important; }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label { color: #89B4FA !important; }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #4361EE 0%, #7209B7 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 28px; }
    .main-header p  { color: rgba(255,255,255,0.85); margin: 6px 0 0; font-size: 14px; }

    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #212529;
        border-left: 4px solid #4361EE;
        padding-left: 10px;
        margin: 24px 0 16px;
    }

    /* Chart containers */
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }

    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #EFF6FF, #F0FDF4);
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .insight-box p { margin: 4px 0; font-size: 14px; color: #1E40AF; }

    /* Tab styling */
    .stTabs [role="tablist"] { border-bottom: 2px solid #E9ECEF; }
    .stTabs [role="tab"][aria-selected="true"] { color: #4361EE !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/expenses.csv"):
        df_raw = generate_expenses()
        df_raw.to_csv("data/expenses.csv", index=False)
    return load_and_clean("data/expenses.csv")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Dashboard Controls")
    st.markdown("---")

    df_full = get_data()

    # Month filter
    months = sorted(df_full["month"].unique())
    month_labels = sorted(df_full["month_name"].unique(),
                          key=lambda x: df_full[df_full["month_name"] == x]["date"].min())
    selected_months = st.multiselect(
        "📅 Filter by Month",
        options=month_labels,
        default=month_labels,
    )

    # Category filter
    all_cats = sorted(df_full["category"].unique())
    selected_cats = st.multiselect(
        "🏷️ Filter by Category",
        options=all_cats,
        default=all_cats,
    )

    # Payment filter
    all_pays = sorted(df_full["payment_method"].unique())
    selected_pays = st.multiselect(
        "💳 Filter by Payment",
        options=all_pays,
        default=all_pays,
    )

    st.markdown("---")
    budget = st.number_input("💰 Monthly Budget (₹)", min_value=0, value=30000, step=1000)

    st.markdown("---")
    regenerate = st.button("🔄 Re-generate Data")
    if regenerate:
        df_new = generate_expenses()
        df_new.to_csv("data/expenses.csv", index=False)
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("**📁 Project Links**")
    st.markdown("🐙 [GitHub Repo](#)")
    st.markdown("📄 [README](#)")
    st.markdown("---")
    st.caption("Personal Expense Tracker v1.0\nBuilt with Python + Streamlit")


# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_full[
    df_full["month_name"].isin(selected_months) &
    df_full["category"].isin(selected_cats) &
    df_full["payment_method"].isin(selected_pays)
].copy()

if df.empty:
    st.warning("⚠️ No data matches your filters. Please adjust the sidebar selections.")
    st.stop()


# ── Pre-compute summaries ─────────────────────────────────────────────────────
cat  = category_summary(df)
mon  = monthly_summary(df)
pay  = payment_method_summary(df)
dai  = daily_spending(df)
wkd  = weekday_summary(df)
top  = top_expenses(df, 10)
met  = key_metrics(df)


# ╔══════════════════════════════════════════════════════════════╗
# ║  HEADER                                                      ║
# ╚══════════════════════════════════════════════════════════════╝
st.markdown("""
<div class="main-header">
    <h1>💰 Personal Expense Tracker</h1>
    <p>Interactive financial analytics dashboard — track, analyse & visualise your spending</p>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  KPI METRICS ROW                                             ║
# ╚══════════════════════════════════════════════════════════════╝
st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("💸 Total Spent",     f"₹{met['total_spent']:,.0f}")
k2.metric("🔢 Transactions",    met["total_transactions"])
k3.metric("📆 Avg / Day",       f"₹{met['avg_daily_spending']:,.0f}")
k4.metric("📋 Avg / Txn",       f"₹{met['avg_transaction']:,.0f}")
k5.metric("🏆 Top Category",    met["highest_category"])
k6.metric("💳 Top Payment",     met["most_used_payment"])

# Budget tracker
if budget > 0 and len(selected_months) > 0:
    avg_monthly = met["total_spent"] / max(met["months_covered"], 1)
    budget_pct  = min(avg_monthly / budget * 100, 100)
    status      = "🟢" if budget_pct < 80 else ("🟡" if budget_pct < 100 else "🔴")
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:16px 20px;
                box-shadow:0 2px 8px rgba(0,0,0,.06);margin:16px 0;">
        <b>{status} Monthly Budget Tracker</b>
        <p style="margin:6px 0;font-size:13px;color:#555;">
            Avg monthly spend: ₹{avg_monthly:,.0f} / Budget: ₹{budget:,.0f}
            &nbsp;|&nbsp; Used: {budget_pct:.1f}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(int(budget_pct))

st.markdown("---")


# ╔══════════════════════════════════════════════════════════════╗
# ║  TABS                                                        ║
# ╚══════════════════════════════════════════════════════════════╝
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏷️ Categories",
    "📅 Monthly Trends",
    "💳 Payment Analysis",
    "📆 Daily Patterns",
    "📋 Transaction Log",
    "📄 Report",
])


# ── TAB 1 : Categories ────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">🏷️ Spending by Category</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([6, 4])

    with c1:
        # Interactive Plotly bar
        fig_bar = px.bar(
            cat, x="total_amount", y="category",
            orientation="h",
            color="total_amount",
            color_continuous_scale="Blues",
            text=cat["total_amount"].apply(lambda x: f"₹{x:,.0f}"),
            labels={"total_amount": "Total (₹)", "category": "Category"},
            title="Category-wise Total Spending",
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="white", paper_bgcolor="white",
            height=420, margin=dict(l=10, r=60, t=40, b=10),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        # Donut chart
        fig_donut = px.pie(
            cat, values="total_amount", names="category",
            hole=0.5, title="Category Share (%)",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut.update_layout(
            showlegend=False, height=420,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown('<div class="section-header">📊 Category Summary Table</div>', unsafe_allow_html=True)
    display_cat = cat.copy()
    display_cat["total_amount"] = display_cat["total_amount"].apply(lambda x: f"₹{x:,.2f}")
    display_cat["avg_per_transaction"] = display_cat["avg_per_transaction"].apply(lambda x: f"₹{x:,.2f}")
    display_cat["percentage"] = display_cat["percentage"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(display_cat, use_container_width=True, height=300)


# ── TAB 2 : Monthly Trends ────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">📈 Monthly Spending Trend</div>', unsafe_allow_html=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=mon["month_name"], y=mon["total"],
        mode="lines+markers+text",
        name="Monthly Total",
        line=dict(color="#4361EE", width=3),
        marker=dict(size=10, color="#4361EE", line=dict(color="white", width=2)),
        text=[f"₹{v:,.0f}" for v in mon["total"]],
        textposition="top center",
        fill="tozeroy", fillcolor="rgba(67,97,238,0.08)",
    ))
    if budget > 0:
        fig_line.add_hline(y=budget, line_dash="dot", line_color="#E63946",
                           annotation_text=f"Budget ₹{budget:,.0f}",
                           annotation_position="bottom right")
    fig_line.update_layout(
        title="Monthly Spending vs Budget",
        xaxis_title="Month", yaxis_title="Total (₹)",
        plot_bgcolor="white", paper_bgcolor="white",
        height=420, margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(tickformat="₹,.0f"),
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Stacked bar by category
    st.markdown('<div class="section-header">📊 Monthly Spend by Category (Stacked)</div>', unsafe_allow_html=True)
    pivot = df.pivot_table(index="month_name", columns="category",
                           values="amount", aggfunc="sum").fillna(0)
    month_order = (df.drop_duplicates("month_name")
                     .sort_values("month")["month_name"].tolist())
    pivot = pivot.reindex(month_order)

    fig_stack = px.bar(
        pivot.reset_index().melt(id_vars="month_name"),
        x="month_name", y="value", color="category",
        barmode="stack",
        labels={"value": "Amount (₹)", "month_name": "Month", "category": "Category"},
        title="Monthly Category Breakdown",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_stack.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=420, margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.4),
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown('<div class="section-header">Monthly Summary Table</div>', unsafe_allow_html=True)
    disp_mon = mon[["month_name", "total", "transactions"]].copy()
    disp_mon["total"] = disp_mon["total"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(disp_mon, use_container_width=True, height=250)


# ── TAB 3 : Payment Analysis ──────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">💳 Payment Method Analysis</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)

    with p1:
        fig_pie = px.pie(
            pay, values="total_amount", names="payment_method",
            title="Spend by Payment Method",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.3,
        )
        fig_pie.update_traces(textinfo="percent+label+value",
                              texttemplate="%{label}<br>%{percent}<br>₹%{value:,.0f}")
        fig_pie.update_layout(showlegend=False, height=420,
                              plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    with p2:
        fig_pay_bar = px.bar(
            pay, x="payment_method", y="total_amount",
            color="total_amount", color_continuous_scale="Teal",
            text=pay["total_amount"].apply(lambda x: f"₹{x:,.0f}"),
            title="Payment Method Total Spend",
            labels={"total_amount": "Total (₹)", "payment_method": "Method"},
        )
        fig_pay_bar.update_traces(textposition="outside")
        fig_pay_bar.update_layout(
            coloraxis_showscale=False, height=420,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_pay_bar, use_container_width=True)

    # Payment × Category heatmap
    st.markdown('<div class="section-header">🔥 Payment × Category Heatmap</div>', unsafe_allow_html=True)
    heat_df = df.pivot_table(index="payment_method", columns="category",
                             values="amount", aggfunc="sum").fillna(0)
    fig_heat = px.imshow(
        heat_df, text_auto=".0f", aspect="auto",
        color_continuous_scale="Blues",
        title="Amount Spent: Payment Method × Category",
    )
    fig_heat.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig_heat, use_container_width=True)


# ── TAB 4 : Daily Patterns ────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">📅 Daily Spending Trend</div>', unsafe_allow_html=True)

    fig_daily = go.Figure()
    fig_daily.add_trace(go.Bar(
        x=dai["date"], y=dai["daily_total"],
        name="Daily Spend",
        marker_color="rgba(67,97,238,0.45)",
    ))
    fig_daily.add_trace(go.Scatter(
        x=dai["date"], y=dai["7d_rolling"],
        name="7-Day Rolling Avg",
        line=dict(color="#E63946", width=2.5),
    ))
    fig_daily.update_layout(
        title="Daily Spending with 7-Day Rolling Average",
        xaxis_title="Date", yaxis_title="Amount (₹)",
        plot_bgcolor="white", paper_bgcolor="white",
        height=420, legend=dict(orientation="h", y=1.08),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown('<div class="section-header">📆 Spending by Day of Week</div>', unsafe_allow_html=True)
    fig_wkd = px.bar(
        wkd, x="day_of_week", y="avg_amount",
        color="avg_amount", color_continuous_scale="Purples",
        text=wkd["avg_amount"].apply(lambda x: f"₹{x:,.0f}"),
        title="Average Spending per Day of Week",
        labels={"avg_amount": "Avg (₹)", "day_of_week": "Day"},
    )
    fig_wkd.update_traces(textposition="outside")
    fig_wkd.update_layout(
        coloraxis_showscale=False, height=380,
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_wkd, use_container_width=True)


# ── TAB 5 : Transaction Log ───────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">📋 Transaction Log</div>', unsafe_allow_html=True)

    # Search
    search = st.text_input("🔍 Search notes / categories", "")
    display_df = df.copy()
    if search:
        mask = (display_df["note"].str.contains(search, case=False, na=False) |
                display_df["category"].str.contains(search, case=False, na=False))
        display_df = display_df[mask]

    display_df2 = display_df[["date", "category", "amount", "payment_method", "note"]].copy()
    display_df2["date"] = display_df2["date"].dt.strftime("%d %b %Y")
    display_df2["amount"] = display_df2["amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(display_df2, use_container_width=True, height=500)

    st.markdown('<div class="section-header">🔝 Top 10 Largest Expenses</div>', unsafe_allow_html=True)
    disp_top = top.copy()
    disp_top["date"]   = disp_top["date"].dt.strftime("%d %b %Y")
    disp_top["amount"] = disp_top["amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(disp_top, use_container_width=True, height=320)

    # Download button
    csv_data = df[["date", "category", "amount", "payment_method", "note"]].copy()
    csv_data["date"] = csv_data["date"].dt.strftime("%Y-%m-%d")
    csv_bytes = csv_data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV",
                       data=csv_bytes, file_name="filtered_expenses.csv",
                       mime="text/csv")


# ── TAB 6 : Report ────────────────────────────────────────────────────────────
with tab6:
    st.markdown('<div class="section-header">📄 Auto-Generated Expense Report</div>', unsafe_allow_html=True)

    report_text = generate_text_report(df)
    st.code(report_text, language="text")

    st.download_button(
        "⬇️ Download Full Report (.txt)",
        data=report_text.encode("utf-8"),
        file_name="expense_report.txt",
        mime="text/plain",
    )

    # Insights panel
    st.markdown('<div class="section-header">💡 Smart Insights</div>', unsafe_allow_html=True)
    top_cat = cat.iloc[0]
    avg_m   = met["total_spent"] / max(met["months_covered"], 1)

    insights = [
        f"🏆 Your #1 spending category is **{top_cat['category']}** "
        f"({top_cat['percentage']}% — ₹{top_cat['total_amount']:,.0f} total).",
        f"📆 You spend an average of **₹{met['avg_daily_spending']:,.0f} per day** "
        f"across {met['date_range_days']} days.",
        f"💳 **{met['most_used_payment']}** is your preferred payment method.",
        f"💸 Your single largest purchase was **₹{met['highest_single']:,.0f}**.",
        f"📊 Monthly average: **₹{avg_m:,.0f}**. " +
        ("Consider reviewing non-essential expenses." if avg_m > budget else "You're within budget 🎉"),
    ]
    for ins in insights:
        st.markdown(f"""
        <div class="insight-box"><p>{ins}</p></div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6C757D; font-size:13px; padding:8px 0;">
    💰 Personal Expense Tracker | Built with Python · Pandas · Plotly · Streamlit
    &nbsp;|&nbsp; A Python Course Project
</div>
""", unsafe_allow_html=True)
