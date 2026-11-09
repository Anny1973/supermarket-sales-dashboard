# 🛒 Supermarket Sales Dashboard

An interactive business intelligence dashboard built with Streamlit and
Plotly to analyze supermarket sales, profitability, customer behavior,
product performance and branch performance.

![Executive Summary](screenshots/executive-summary.png)

## Features
- Sidebar filters: date range, branch, city, customer type, gender,
  product line and payment method
- Executive KPIs: total sales, profit, orders, quantity, average rating
- Business indicators: revenue/order, quantity/order, profit/order
- Automatically generated insights: top performers, profitability,
  risk areas and recommendations
- Tabbed analysis: Executive Overview, Products, Customers,
  Time Analysis, Branch & City
- Interactive Plotly charts (bar, line, pie)
- Filtered transaction table with CSV download

## Tech Stack
Python · Streamlit · Pandas · Plotly

## Dataset
Supermarket sales dataset with 1,000 transactions across three
branches (Yangon, Mandalay, Naypyitaw), January–March 2019.

## Getting Started
```bash
git clone https://github.com/<your-username>/supermarket-sales-dashboard.git
cd supermarket-sales-dashboard
pip install -r requirements.txt
streamlit run supermarket_dashboard.py
```

## Key Insights (from the default view)
- Total sales: 322,966.75 across 1,000 orders
- Top branch: C (Naypyitaw)
- Top product line by sales: Food and beverages
- Peak sales hour: 19:00

## Future Improvements
- Sales forecasting
- Customer segmentation
- Deployment on Streamlit Community Cloud
