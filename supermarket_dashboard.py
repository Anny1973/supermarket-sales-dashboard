
# ============================================================
# SUPERMARKET SALES DASHBOARD
# Clean Streamlit Version
# Online Dataset - No CSV Upload Required
# ============================================================

import streamlit as st
import pandas as pd
import requests
import urllib3
import plotly.express as px
from io import StringIO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .kpi-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background-color: rgba(128, 128, 128, 0.08);
        text-align: center;
        margin-bottom: 10px;
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 25px;
        font-weight: 700;
    }

    .insight-card {
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background-color: rgba(128, 128, 128, 0.06);
        min-height: 110px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .insight-value {
        font-size: 20px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ONLINE DATA SOURCE
# ============================================================

DATA_URL = (
    "https://huggingface.co/spaces/Andreean/"
    "Visualisasi_Sales_Supermarket/resolve/main/"
    "supermarket_sales%20-%20Sheet1.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        DATA_URL,
        headers=headers,
        verify=False,
        timeout=30
    )

    response.raise_for_status()

    data = pd.read_csv(
        StringIO(response.text)
    )

    return data


# ============================================================
# LOAD DATA WITH ERROR HANDLING
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "❌ Unable to load the online supermarket dataset."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("%", "percent")
)


# ============================================================
# DATE AND TIME PROCESSING
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["hour"] = pd.to_datetime(
    df["time"].astype(str),
    format="%H:%M",
    errors="coerce"
).dt.hour

df["year"] = df["date"].dt.year

df["month"] = df["date"].dt.month

df["month_name"] = df["date"].dt.strftime(
    "%B"
)

df["day_name"] = df["date"].dt.day_name()


# ============================================================
# PROFESSIONAL DASHBOARD HEADER
# ============================================================

st.markdown(
"""
<div style="
background: linear-gradient(135deg, #1f2937, #374151);
padding: 22px 28px;
border-radius: 15px;
margin-bottom: 25px;
">

<h1 style="
color: white;
margin: 0;
font-size: 36px;
">
🛒 Supermarket Sales Dashboard
</h1>

<p style="
color: #d1d5db;
font-size: 17px;
margin-top: 8px;
margin-bottom: 0;
">
Interactive business intelligence dashboard for sales, profitability, customers, products and branch performance
</p>

</div>
""",
unsafe_allow_html=True
)

# ============================================================
# ADVANCED SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("## 🎛️ Dashboard Filters")

# ------------------------------------------------------------
# Date Filter
# ------------------------------------------------------------

st.sidebar.markdown("### 📅 Date Range")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ------------------------------------------------------------
# Location Filters
# ------------------------------------------------------------

st.sidebar.markdown("### 📍 Location")

selected_branch = st.sidebar.multiselect(
    "Branch",
    options=sorted(df["branch"].unique()),
    default=sorted(df["branch"].unique())
)

selected_city = st.sidebar.multiselect(
    "City",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

# ------------------------------------------------------------
# Customer Filters
# ------------------------------------------------------------

st.sidebar.markdown("### 👥 Customer")

selected_customer_type = st.sidebar.multiselect(
    "Customer Type",
    options=sorted(df["customer_type"].unique()),
    default=sorted(df["customer_type"].unique())
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["gender"].unique()),
    default=sorted(df["gender"].unique())
)

# ------------------------------------------------------------
# Product Filter
# ------------------------------------------------------------

st.sidebar.markdown("### 🛍️ Product")

selected_product_line = st.sidebar.multiselect(
    "Product Line",
    options=sorted(df["product_line"].unique()),
    default=sorted(df["product_line"].unique())
)

# ------------------------------------------------------------
# Payment Filter
# ------------------------------------------------------------

st.sidebar.markdown("### 💳 Payment")

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["payment"].unique()),
    default=sorted(df["payment"].unique())
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_branch:
    filtered_df = filtered_df[
        filtered_df["branch"].isin(selected_branch)
    ]


if selected_city:
    filtered_df = filtered_df[
        filtered_df["city"].isin(selected_city)
    ]


if selected_customer_type:
    filtered_df = filtered_df[
        filtered_df["customer_type"].isin(selected_customer_type)
    ]


if selected_gender:
    filtered_df = filtered_df[
        filtered_df["gender"].isin(selected_gender)
    ]


if selected_product_line:
    filtered_df = filtered_df[
        filtered_df["product_line"].isin(selected_product_line)
    ]


if selected_payment:
    filtered_df = filtered_df[
        filtered_df["payment"].isin(selected_payment)
    ]

# ============================================================
# FILTER STATUS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Filter Status")

st.sidebar.metric(
    "Transactions",
    f"{len(filtered_df):,}"
)

st.sidebar.metric(
    "Sales",
    f"${filtered_df['total'].sum():,.2f}"
)    

# ------------------------------------------------------------
# Apply Date Filter
# ------------------------------------------------------------

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date) &
        (filtered_df["date"].dt.date <= end_date)
    ]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data matches the selected filters. "
        "Please change the filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["total"].sum()

total_profit = filtered_df["gross_income"].sum()

total_orders = filtered_df["invoice_id"].nunique()

total_quantity = filtered_df["quantity"].sum()

average_rating = filtered_df["rating"].mean()


if total_orders > 0:

    average_order_value = (
        total_sales / total_orders
    )

else:

    average_order_value = 0


if total_sales > 0:

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = 0

# ============================================================
# OVERALL PROFIT MARGIN
# ============================================================

overall_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0
    else 0
)
# ============================================================
# ADVANCED KPI CALCULATIONS
# ============================================================

revenue_per_order = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

quantity_per_order = (
    total_quantity / total_orders
    if total_orders > 0
    else 0
)

profit_per_order = (
    total_profit / total_orders
    if total_orders > 0
    else 0
)

revenue_per_quantity = (
    total_sales / total_quantity
    if total_quantity > 0
    else 0
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

branch_sales = (
    filtered_df
    .groupby("branch")["total"]
    .sum()
)

best_branch = branch_sales.idxmax()

best_branch_sales = branch_sales.max()


city_sales = (
    filtered_df
    .groupby("city")["total"]
    .sum()
)

best_city = city_sales.idxmax()

best_city_sales = city_sales.max()


product_sales = (
    filtered_df
    .groupby("product_line")["total"]
    .sum()
)

best_product = product_sales.idxmax()

best_product_sales = product_sales.max()


product_profit = (
    filtered_df
    .groupby("product_line")["gross_income"]
    .sum()
)

best_profit_product = product_profit.idxmax()

best_profit = product_profit.max()


payment_sales = (
    filtered_df
    .groupby("payment")["total"]
    .sum()
)

best_payment = payment_sales.idxmax()


hour_sales = (
    filtered_df
    .groupby("hour")["total"]
    .sum()
)

peak_hour = hour_sales.idxmax()

peak_hour_sales = hour_sales.max()


customer_type_sales = (
    filtered_df
    .groupby("customer_type")["total"]
    .sum()
)

best_customer = customer_type_sales.idxmax()


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📊 Executive Summary</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROFESSIONAL KPI CARDS
# ============================================================

st.markdown(
    """
    <div style="
        margin-top: 10px;
        margin-bottom: 15px;
    ">
        <h2 style="
            margin-bottom: 3px;
        ">
            📊 Executive Performance
        </h2>
        <p style="
            color: #6b7280;
            margin-top: 0;
        ">
            Key business performance indicators for the selected filters
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.2f}"
    )

with k2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.2f}"
    )

with k3:
    st.metric(
        label="🧾 Total Orders",
        value=f"{total_orders:,}"
    )

with k4:
    st.metric(
        label="📦 Quantity Sold",
        value=f"{total_quantity:,}"
    )

with k5:
    st.metric(
        label="⭐ Average Rating",
        value=f"{average_rating:.2f}"
    )


# ============================================================
# EXECUTIVE TREND INDICATORS
# ============================================================

st.markdown(
    """
    <div style="margin-top:25px;margin-bottom:15px;">
        <h3>📈 Business Performance Indicators</h3>
        <p style="color:#6b7280;">
            Additional metrics for evaluating sales efficiency and profitability
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

indicator_col1, indicator_col2, indicator_col3, indicator_col4 = st.columns(4)

with indicator_col1:
    st.metric(
        "💵 Revenue / Order",
        f"${revenue_per_order:,.2f}"
    )

with indicator_col2:
    st.metric(
        "📦 Quantity / Order",
        f"{quantity_per_order:.2f}"
    )

with indicator_col3:
    st.metric(
        "💰 Profit / Order",
        f"${profit_per_order:,.2f}"
    )

with indicator_col4:
    st.metric(
        "🏷️ Revenue / Unit",
        f"${revenue_per_quantity:,.2f}"
    )

# ============================================================
# BUSINESS PERFORMANCE SUMMARY
# ============================================================

st.markdown(
    """
    <div style="margin-top:30px;margin-bottom:15px;">
        <h3>🧠 Business Performance Summary</h3>
    </div>
    """,
    unsafe_allow_html=True
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"""
        **Sales Performance**

        The dashboard records **{total_orders:,} orders** with total
        sales of **${total_sales:,.2f}**.

        Average revenue generated per order is
        **${revenue_per_order:,.2f}**.
        """
    )

with summary_col2:

    st.success(
        f"""
        **Profitability Performance**

        Total gross income is **${total_profit:,.2f}** with an
        overall profit margin of **{overall_margin:.2f}%**.

        Average profit generated per order is
        **${profit_per_order:,.2f}**.
        """
    )

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Executive Overview</div>',
    unsafe_allow_html=True
)

overview_df = pd.DataFrame({
    "Metric": [
        "Sales",
        "Profit",
        "Orders",
        "Quantity"
    ],
    "Value": [
        total_sales,
        total_profit,
        total_orders,
        total_quantity
    ]
})

fig_overview = px.bar(
    overview_df,
    x="Metric",
    y="Value",
    title="Overall Business Performance",
    text_auto=".2f"
)

fig_overview.update_layout(
    xaxis_title="Metric",
    yaxis_title="Value"
)

st.plotly_chart(
    fig_overview,
    use_container_width=True,
    key="executive_overview"
)

# ============================================================
# ADVANCED KPIs
# ============================================================

st.markdown(
    '<div class="section-title">📈 Advanced KPIs</div>',
    unsafe_allow_html=True
)

adv1, adv2, adv3, adv4 = st.columns(4)


with adv1:

    st.metric(
        "Revenue / Order",
        f"₹{revenue_per_order:,.2f}"
    )


with adv2:

    st.metric(
        "Quantity / Order",
        f"{quantity_per_order:.2f}"
    )


with adv3:

    st.metric(
        "Profit / Order",
        f"₹{profit_per_order:,.2f}"
    )


with adv4:

    st.metric(
        "Revenue / Item",
        f"₹{revenue_per_quantity:,.2f}"
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True
)


ins1, ins2, ins3 = st.columns(3)


with ins1:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🏆 Best Branch</div>
            <div class="insight-value">{best_branch}</div>
            <div>Sales: ₹{best_branch_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with ins2:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🏙️ Best City</div>
            <div class="insight-value">{best_city}</div>
            <div>Sales: ₹{best_city_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with ins3:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🛍️ Best Product</div>
            <div class="insight-value">{best_product}</div>
            <div>Sales: ₹{best_product_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


ins4, ins5, ins6 = st.columns(3)


with ins4:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">💰 Most Profitable Product</div>
            <div class="insight-value">{best_profit_product}</div>
            <div>Profit: ₹{best_profit:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with ins5:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">💳 Top Payment Method</div>
            <div class="insight-value">{best_payment}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with ins6:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">⏰ Peak Sales Hour</div>
            <div class="insight-value">{int(peak_hour):02d}:00</div>
            <div>Sales: ₹{peak_hour_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KPI SUMMARY TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 KPI Summary</div>',
    unsafe_allow_html=True
)

kpi_summary = pd.DataFrame(
    {
        "Metric": [
            "Total Sales",
            "Total Profit",
            "Total Orders",
            "Total Quantity",
            "Average Rating",
            "Average Order Value",
            "Profit Margin",
            "Revenue / Order",
            "Quantity / Order",
            "Profit / Order",
            "Revenue / Item"
        ],
        "Value": [
            f"₹{total_sales:,.2f}",
            f"₹{total_profit:,.2f}",
            f"{total_orders:,}",
            f"{total_quantity:,}",
            f"{average_rating:.2f}",
            f"₹{average_order_value:,.2f}",
            f"{profit_margin:.2f}%",
            f"₹{revenue_per_order:,.2f}",
            f"{quantity_per_order:.2f}",
            f"₹{profit_per_order:,.2f}",
            f"₹{revenue_per_quantity:,.2f}"
        ]
    }
)

st.dataframe(
    kpi_summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PREPARE ANALYSIS DATASETS
# ============================================================


# ------------------------------------------------------------
# Product Analysis
# ------------------------------------------------------------

product_sales_df = (
    filtered_df
    .groupby("product_line", as_index=False)["total"]
    .sum()
    .sort_values("total", ascending=False)
)

product_profit_df = (
    filtered_df
    .groupby("product_line", as_index=False)["gross_income"]
    .sum()
    .sort_values("gross_income", ascending=False)
)


# ============================================================
# PROFIT MARGIN ANALYSIS
# ============================================================

profit_margin_df = (
    filtered_df
    .groupby("product_line")
    .agg(
        Sales=("total", "sum"),
        Profit=("gross_income", "sum")
    )
    .reset_index()
)

profit_margin_df["Profit Margin %"] = (
    profit_margin_df["Profit"]
    / profit_margin_df["Sales"]
    * 100
)

profit_margin_df = profit_margin_df.sort_values(
    "Profit Margin %",
    ascending=False
)

# ============================================================
# TOP / BOTTOM PRODUCTS
# ============================================================

top_5_products = (
    product_sales_df
    .sort_values("total", ascending=False)
    .head(5)
)

bottom_5_products = (
    product_sales_df
    .sort_values("total", ascending=True)
    .head(5)
)


# ------------------------------------------------------------
# Payment Analysis
# ------------------------------------------------------------

payment_sales_df = (
    filtered_df
    .groupby("payment", as_index=False)["total"]
    .sum()
    .sort_values("total", ascending=False)
)


# ------------------------------------------------------------
# Customer Analysis
# ------------------------------------------------------------

customer_type_sales_df = (
    filtered_df
    .groupby("customer_type", as_index=False)["total"]
    .sum()
)

customer_gender_sales_df = (
    filtered_df
    .groupby(
        ["customer_type", "gender"],
        as_index=False
    )["total"]
    .sum()
)

customer_type_profit_df = (
    filtered_df
    .groupby("customer_type", as_index=False)["gross_income"]
    .sum()
)

customer_gender_profit_df = (
    filtered_df
    .groupby(
        ["customer_type", "gender"],
        as_index=False
    )["gross_income"]
    .sum()
)


# ------------------------------------------------------------
# Gender Analysis
# ------------------------------------------------------------

gender_sales_df = (
    filtered_df
    .groupby("gender", as_index=False)["total"]
    .sum()
)


# ------------------------------------------------------------
# Branch Analysis
# ------------------------------------------------------------

branch_sales_df = (
    filtered_df
    .groupby("branch", as_index=False)["total"]
    .sum()
)

branch_profit_df = (
    filtered_df
    .groupby("branch", as_index=False)["gross_income"]
    .sum()
)

# ============================================================
# BRANCH PERFORMANCE
# ============================================================

branch_performance_df = (
    filtered_df
    .groupby("branch")
    .agg(
        Sales=("total", "sum"),
        Profit=("gross_income", "sum"),
        Orders=("invoice_id", "nunique"),
        Quantity=("quantity", "sum"),
        Rating=("rating", "mean")
    )
    .reset_index()
)

branch_performance_df["Profit Margin %"] = (
    branch_performance_df["Profit"]
    / branch_performance_df["Sales"]
    * 100
)

branch_performance_df = branch_performance_df.sort_values(
    "Sales",
    ascending=False
)

# ------------------------------------------------------------
# City Analysis
# ------------------------------------------------------------

city_sales_df = (
    filtered_df
    .groupby("city", as_index=False)["total"]
    .sum()
)


# ------------------------------------------------------------
# Daily Analysis
# ------------------------------------------------------------

daily_sales_df = (
    filtered_df
    .groupby("date", as_index=False)["total"]
    .sum()
    .sort_values("date")
)


# ------------------------------------------------------------
# Monthly Analysis
# ------------------------------------------------------------

monthly_sales_df = (
    filtered_df
    .groupby(
        ["year", "month", "month_name"],
        as_index=False
    )["total"]
    .sum()
    .sort_values(["year", "month"])
)

monthly_sales_df["period"] = (
    monthly_sales_df["month_name"]
    + " "
    + monthly_sales_df["year"].astype(str)
)


# ------------------------------------------------------------
# Hourly Analysis
# ------------------------------------------------------------

hourly_sales_df = (
    filtered_df
    .groupby("hour", as_index=False)["total"]
    .sum()
    .sort_values("hour")
)


# ------------------------------------------------------------
# Day of Week Analysis
# ------------------------------------------------------------

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_sales_df = (
    filtered_df
    .groupby("day_name", as_index=False)["total"]
    .sum()
)

day_sales_df["day_name"] = pd.Categorical(
    day_sales_df["day_name"],
    categories=day_order,
    ordered=True
)

day_sales_df = day_sales_df.sort_values(
    "day_name"
)

# ============================================================
# AUTOMATED BUSINESS INSIGHTS
# ============================================================

overall_margin = (
    total_profit / total_sales * 100
    if total_sales > 0
    else 0
)

best_margin_product = (
    profit_margin_df.iloc[0]["product_line"]
)

best_margin_value = (
    profit_margin_df.iloc[0]["Profit Margin %"]
)

lowest_margin_product = (
    profit_margin_df.iloc[-1]["product_line"]
)

lowest_margin_value = (
    profit_margin_df.iloc[-1]["Profit Margin %"]
)

highest_branch = (
    branch_performance_df.iloc[0]["branch"]
)

highest_branch_sales = (
    branch_performance_df.iloc[0]["Sales"]
)

highest_customer_type = (
    customer_type_sales_df
    .sort_values("total", ascending=False)
    .iloc[0]["customer_type"]
)

# ============================================================
# STRONGER AUTOMATED BUSINESS INSIGHTS
# ============================================================

# -----------------------------
# Top Performer
# -----------------------------

top_product_row = (
    product_sales_df
    .sort_values("total", ascending=False)
    .iloc[0]
)

top_product = top_product_row["product_line"]
top_product_sales = top_product_row["total"]

# -----------------------------
# Most Profitable Product
# -----------------------------

top_profit_row = (
    product_profit_df
    .sort_values("gross_income", ascending=False)
    .iloc[0]
)

top_profit_product = top_profit_row["product_line"]
top_profit_value = top_profit_row["gross_income"]

# -----------------------------
# Lowest Margin Product
# -----------------------------

lowest_margin_product = (
    profit_margin_df
    .sort_values("Profit Margin %")
    .iloc[0]["product_line"]
)

lowest_margin_value = (
    profit_margin_df
    .sort_values("Profit Margin %")
    .iloc[0]["Profit Margin %"]
)

# -----------------------------
# Highest Performing Branch
# -----------------------------

highest_branch_row = (
    branch_performance_df
    .sort_values("Sales", ascending=False)
    .iloc[0]
)

highest_branch = highest_branch_row["branch"]
highest_branch_sales = highest_branch_row["Sales"]

# -----------------------------
# Lowest Performing Branch
# -----------------------------

lowest_branch_row = (
    branch_performance_df
    .sort_values("Sales")
    .iloc[0]
)

lowest_branch = lowest_branch_row["branch"]
lowest_branch_sales = lowest_branch_row["Sales"]

# -----------------------------
# Highest Customer Type
# -----------------------------

highest_customer_type = (
    customer_type_sales_df
    .sort_values("total", ascending=False)
    .iloc[0]["customer_type"]
)

# ============================================================
# AUTOMATED BUSINESS INSIGHTS
# ============================================================

st.markdown(
    """
    <div style="
        margin-top: 30px;
        margin-bottom: 20px;
    ">
        <h2>🤖 Automated Business Insights</h2>
        <p style="color:#6b7280;">
            Automatically generated insights from the selected sales data
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TOP PERFORMER
# ============================================================

st.markdown("### 🏆 Top Performer")

c1, c2 = st.columns(2)

with c1:
    st.success(
        f"**Top Selling Product**\n\n"
        f"{top_product}\n\n"
        f"Sales: ${top_product_sales:,.2f}"
    )

with c2:
    st.success(
        f"**Top Performing Branch**\n\n"
        f"Branch {highest_branch}\n\n"
        f"Sales: ${highest_branch_sales:,.2f}"
    )


# ============================================================
# PROFITABILITY
# ============================================================

st.markdown("### 💰 Profitability")

c3, c4 = st.columns(2)

with c3:
    st.info(
        f"**Most Profitable Product**\n\n"
        f"{top_profit_product}\n\n"
        f"Gross Income: ${top_profit_value:,.2f}"
    )

with c4:
    st.info(
        f"**Overall Profit Margin**\n\n"
        f"{overall_margin:.2f}%"
    )


# ============================================================
# RISK AREA
# ============================================================

st.markdown("### ⚠️ Risk Area")

c5, c6 = st.columns(2)

with c5:
    st.warning(
        f"**Lowest Margin Product**\n\n"
        f"{lowest_margin_product}\n\n"
        f"Margin: {lowest_margin_value:.2f}%"
    )

with c6:
    st.warning(
        f"**Lowest Performing Branch**\n\n"
        f"Branch {lowest_branch}\n\n"
        f"Sales: ${lowest_branch_sales:,.2f}"
    )


# ============================================================
# RECOMMENDATION
# ============================================================

st.markdown("### 💡 Recommendation")

if lowest_margin_value < overall_margin:
    recommendation = (
        f"Review the pricing, costs and product mix of "
        f"**{lowest_margin_product}**, as its profit margin "
        f"({lowest_margin_value:.2f}%) is below the overall "
        f"business margin ({overall_margin:.2f}%)."
    )
else:
    recommendation = (
        f"Continue monitoring product margins and focus on "
        f"high-performing products such as **{top_profit_product}** "
        f"to maintain profitability."
    )

st.info(recommendation)

# ============================================================
# PROFESSIONAL CHART STYLE
# ============================================================

professional_layout = dict(
    template="plotly_white",
    font=dict(
        family="Arial",
        size=13
    ),
    title_font=dict(
        size=20
    ),
    margin=dict(
        l=50,
        r=30,
        t=70,
        b=50
    ),
    hoverlabel=dict(
        font_size=13
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# ============================================================
# DASHBOARD TABS
# ============================================================

tab_overview, tab_products, tab_customers, tab_time, tab_location = st.tabs(
    [
        "📊 Executive Overview",
        "🛍️ Products",
        "👥 Customers",
        "⏱️ Time Analysis",
        "🏢 Branch & City"
    ]
)

with tab_overview:

    st.markdown("## 📊 Executive Overview")

    st.caption(
        "Business performance based on the currently selected filters."
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric(
            "Filtered Transactions",
            f"{len(filtered_df):,}"
        )

    with summary_col2:
        st.metric(
            "Filtered Sales",
            f"${filtered_df['total'].sum():,.2f}"
        )

    with summary_col3:
        st.metric(
            "Filtered Profit",
            f"${filtered_df['gross_income'].sum():,.2f}"
        )

# Existing Overview charts continue below this point
# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tab_overview:

    st.subheader("📊 Sales Overview")


    # --------------------------------------------------------
    # Sales vs Profit by Product Line
    # --------------------------------------------------------

    sales_profit_df = (
        filtered_df
        .groupby("product_line", as_index=False)
        .agg(
            Sales=("total", "sum"),
            Profit=("gross_income", "sum")
        )
    )

    sales_profit_long = sales_profit_df.melt(
        id_vars="product_line",
        value_vars=["Sales", "Profit"],
        var_name="Metric",
        value_name="Amount"
    )

    fig_sales_profit = px.bar(
        sales_profit_long,
        x="product_line",
        y="Amount",
        color="Metric",
        barmode="group",
        title="Sales vs Profit by Product Line"
    )

    fig_sales_profit.update_layout(
        xaxis_title="Product Line",
        yaxis_title="Amount",
        legend_title="Metric"
    )

    st.plotly_chart(
        fig_sales_profit,
        use_container_width=True,
        key="overview_sales_profit"
    )


    # --------------------------------------------------------
    # Payment Method
    # --------------------------------------------------------

    fig_payment = px.bar(
        payment_sales_df,
        x="payment",
        y="total",
        title="Sales by Payment Method",
        text_auto=".2f"
    )

    fig_payment.update_layout(
        professional_layout,
        xaxis_title="Payment Method",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True,
        key="overview_payment"
    )


    # --------------------------------------------------------
    # Customer Type
    # --------------------------------------------------------

    fig_customer_type = px.bar(
        customer_type_sales_df,
        x="customer_type",
        y="total",
        title="Sales by Customer Type",
        text_auto=".2f"
    )

    fig_customer_type.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_customer_type,
        use_container_width=True,
        key="overview_customer_type"
    )


    # --------------------------------------------------------
    # Gender
    # --------------------------------------------------------

    fig_gender = px.pie(
        gender_sales_df,
        names="gender",
        values="total",
        title="Sales Distribution by Gender"
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True,
        key="overview_gender"
    )


# ============================================================
# TAB 2 - PRODUCTS
# ============================================================

with tab_products:

    st.subheader("🛍️ Product Analysis")


    # --------------------------------------------------------
    # Product Sales
    # --------------------------------------------------------

    fig_product_sales = px.bar(
        product_sales_df,
        x="product_line",
        y="total",
        title="Sales by Product Line",
        text_auto=".2f"
    )

    fig_product_sales.update_layout(
        professional_layout,
        xaxis_title="Product Line",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_product_sales,
        use_container_width=True,
        key="products_sales"
    )


    # --------------------------------------------------------
    # Product Profit
    # --------------------------------------------------------

    fig_product_profit = px.bar(
        product_profit_df,
        x="product_line",
        y="gross_income",
        title="Profit by Product Line",
        text_auto=".2f"
    )

    fig_product_profit.update_layout(
        xaxis_title="Product Line",
        yaxis_title="Gross Income"
    )

    st.plotly_chart(
        fig_product_profit,
        use_container_width=True,
        key="products_profit"
    )

    st.subheader("💰 Profit Margin by Product")

    fig_margin = px.bar(
        profit_margin_df,
        x="product_line",
        y="Profit Margin %",
        title="Profit Margin by Product Line",
        text_auto=".2f"
    )

    fig_margin.update_layout(
        xaxis_title="Product Line",
        yaxis_title="Profit Margin (%)"
    )

    st.plotly_chart(
        fig_margin,
        use_container_width=True,
        key="products_profit_margin"
    )
    st.subheader("🏆 Top & Bottom Products")

    top_col, bottom_col = st.columns(2)

    with top_col:

        st.markdown("### 🟢 Top 5 Products")

        st.dataframe(
            top_5_products,
            use_container_width=True,
            hide_index=True
        )

    with bottom_col:

        st.markdown("### 🔴 Bottom 5 Products")

        st.dataframe(
            bottom_5_products,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # Product Performance Table
    # --------------------------------------------------------

    product_performance = (
        filtered_df
        .groupby("product_line")
        .agg(
            Sales=("total", "sum"),
            Profit=("gross_income", "sum"),
            Quantity=("quantity", "sum"),
            Average_Rating=("rating", "mean"),
            Orders=("invoice_id", "nunique")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    product_performance["Profit Margin %"] = (
        product_performance["Profit"]
        / product_performance["Sales"]
        * 100
    )

    st.subheader("📋 Product Performance")

    st.dataframe(
        product_performance,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 - CUSTOMERS
# ============================================================

with tab_customers:

    st.subheader("👥 Customer Analysis")


    # --------------------------------------------------------
    # Sales by Customer Type & Gender
    # --------------------------------------------------------

    fig_customer_sales = px.bar(
        customer_gender_sales_df,
        x="customer_type",
        y="total",
        color="gender",
        barmode="group",
        title="Sales by Customer Type and Gender",
        text_auto=".2f"
    )

    fig_customer_sales.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_customer_sales,
        use_container_width=True,
        key="customers_sales"
    )


    # --------------------------------------------------------
    # Profit by Customer Type & Gender
    # --------------------------------------------------------

    fig_customer_profit = px.bar(
        customer_gender_profit_df,
        x="customer_type",
        y="gross_income",
        color="gender",
        barmode="group",
        title="Profit by Customer Type and Gender",
        text_auto=".2f"
    )

    fig_customer_profit.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_customer_profit,
        use_container_width=True,
        key="customers_profit"
    )


    # --------------------------------------------------------
    # Customer Performance Table
    # --------------------------------------------------------

    customer_performance = (
        filtered_df
        .groupby("customer_type")
        .agg(
            Sales=("total", "sum"),
            Profit=("gross_income", "sum"),
            Orders=("invoice_id", "nunique"),
            Quantity=("quantity", "sum"),
            Average_Rating=("rating", "mean")
        )
        .reset_index()
    )

    customer_performance["Profit Margin %"] = (
        customer_performance["Profit"]
        / customer_performance["Sales"]
        * 100
    )

    customer_performance["Average Order Value"] = (
        customer_performance["Sales"]
        / customer_performance["Orders"]
    )

    st.subheader("📋 Customer Performance")

    st.dataframe(
        customer_performance,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Top Customer Type
    # --------------------------------------------------------

    st.info(
        f"🏆 Highest sales customer type: "
        f"**{best_customer}**"
    )


# ============================================================
# TAB 4 - TIME ANALYSIS
# ============================================================

with tab_time:

    st.subheader("📅 Time Analysis")


    # --------------------------------------------------------
    # Daily Sales Trend
    # --------------------------------------------------------

    fig_daily = px.line(
        daily_sales_df,
        x="date",
        y="total",
        title="Daily Sales Trend",
        markers=True
    )

    fig_daily.update_layout(
        professional_layout,
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True,
        key="time_daily"
    )


    # --------------------------------------------------------
    # Monthly Sales
    # --------------------------------------------------------

    fig_monthly = px.bar(
        monthly_sales_df,
        x="period",
        y="total",
        title="Monthly Sales",
        text_auto=".2f"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        key="time_monthly"
    )


    # --------------------------------------------------------
    # Hourly Sales
    # --------------------------------------------------------

    fig_hourly = px.line(
        hourly_sales_df,
        x="hour",
        y="total",
        title="Hourly Sales",
        markers=True
    )

    fig_hourly.update_layout(
        xaxis_title="Hour",
        yaxis_title="Sales",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        )
    )

    st.plotly_chart(
        fig_hourly,
        use_container_width=True,
        key="time_hourly"
    )


    # --------------------------------------------------------
    # Sales by Day of Week
    # --------------------------------------------------------

    fig_day = px.bar(
        day_sales_df,
        x="day_name",
        y="total",
        title="Sales by Day of Week",
        text_auto=".2f"
    )

    fig_day.update_layout(
        xaxis_title="Day",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_day,
        use_container_width=True,
        key="time_day"
    )


    # --------------------------------------------------------
    # Peak Hour
    # --------------------------------------------------------

    st.success(
        f"⏰ Peak sales hour: "
        f"**{int(peak_hour):02d}:00 - {int(peak_hour):02d}:59** "
        f"with sales of **₹{peak_hour_sales:,.2f}**."
    )


# ============================================================
# TAB 5 - BRANCH & CITY
# ============================================================

with tab_location:

    st.subheader("📍 Branch & City Analysis")


    # --------------------------------------------------------
    # Sales by Branch
    # --------------------------------------------------------

    st.subheader("🏢 Branch Performance")

    st.dataframe(
        branch_performance_df,
        use_container_width=True,
        hide_index=True
    )
    fig_branch_sales = px.bar(
        branch_sales_df,
        x="branch",
        y="total",
        title="🏢 Sales by Branch",
        text_auto=".2f"
    )

    fig_branch_sales.update_layout(
        professional_layout,
        xaxis_title="Branch",
        yaxis_title="Sales"
    )

    fig_branch_sales.update_traces(
         hovertemplate="<b>Branch:</b> %{x}<br>"
                       "<b>Sales:</b> $%{y:,.2f}<extra></extra>"
    )

    st.plotly_chart(
        fig_branch_sales,
        use_container_width=True,
        key="location_branch_sales"
    )


    # --------------------------------------------------------
    # Sales by City
    # --------------------------------------------------------

    fig_city_sales = px.bar(
        city_sales_df,
        x="city",
        y="total",
        title="🌆 Sales by City",
        text_auto=".2f"
    )

    fig_city_sales.update_layout(
        professional_layout,
        xaxis_title="City",
        yaxis_title="Sales"
    )

    fig_city_sales.update_traces(
        hovertemplate="<b>City:</b> %{x}<br>"
                      "<b>Sales:</b> $%{y:,.2f}<extra></extra>"
    )

    st.plotly_chart(
         fig_city_sales,
         use_container_width=True,
         key="location_city_sales"
    )


    # --------------------------------------------------------
    # Profit by Branch
    # --------------------------------------------------------

    fig_branch_profit = px.bar(
        branch_profit_df,
        x="branch",
        y="gross_income",
        title="💰 Profit by Branch",
        text_auto=".2f"
    )

    fig_branch_profit.update_layout(
        professional_layout,
        xaxis_title="Branch",
        yaxis_title="Profit"
    )

    fig_branch_profit.update_traces(
        hovertemplate="<b>Branch:</b> %{x}<br>"
                      "<b>Profit:</b> $%{y:,.2f}<extra></extra>"
    )

    st.plotly_chart(
        fig_branch_profit,
        use_container_width=True,
        key="location_branch_profit"
    )


    # --------------------------------------------------------
    # Branch Performance Table
    # --------------------------------------------------------

    branch_performance = (
        filtered_df
        .groupby("branch")
        .agg(
            Sales=("total", "sum"),
            Profit=("gross_income", "sum"),
            Orders=("invoice_id", "nunique"),
            Quantity=("quantity", "sum"),
            Average_Rating=("rating", "mean")
        )
        .reset_index()
    )

    branch_performance["Profit Margin %"] = (
        branch_performance["Profit"]
        / branch_performance["Sales"]
        * 100
    )

    st.subheader("📋 Branch Performance")

    st.dataframe(
        branch_performance,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # City Performance Table
    # --------------------------------------------------------

    city_performance = (
        filtered_df
        .groupby("city")
        .agg(
            Sales=("total", "sum"),
            Profit=("gross_income", "sum"),
            Orders=("invoice_id", "nunique"),
            Quantity=("quantity", "sum"),
            Average_Rating=("rating", "mean")
        )
        .reset_index()
    )

    city_performance["Profit Margin %"] = (
        city_performance["Profit"]
        / city_performance["Sales"]
        * 100
    )

    st.subheader("📋 City Performance")

    st.dataframe(
        city_performance,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FILTERED TRANSACTION DATA
# ============================================================

st.markdown(
    '<div class="section-title">📄 Filtered Transaction Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="margin-top:20px;margin-bottom:10px;">
        <h3>📥 Export Dashboard Data</h3>
        <p style="color:#6b7280;">
            Download the currently filtered transaction dataset for
            further analysis or reporting.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="supermarket_filtered_data.csv",
    mime="text/csv",
    use_container_width=True
)


# ============================================================
# PROFESSIONAL FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px;
        color:#6b7280;
        font-size:14px;
    ">
        <b>🛒 Supermarket Sales Dashboard</b><br>
        Interactive Business Intelligence & Sales Analytics<br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
