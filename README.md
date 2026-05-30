# Zomato Product Analytics Dashboard

A production-style **product analytics platform** built with Streamlit and Plotly. This project turns marketplace transaction data into executive-ready KPIs, customer lifecycle segments, partner performance views, and actionable business insights—designed to demonstrate end-to-end analytics thinking for **Product Analyst** and **Data Analyst** roles.

---
## Live Demo 

https://zomato-appuct-analytics-dashboard-fdspucxujzv4gfqufdv8q3.streamlit.app

## Overview

Food delivery marketplaces must answer the same questions every week: *Are we growing? Who is buying again? Which cities and restaurants drive GMV? Which customers are about to churn?*

This dashboard connects **users**, **orders**, **restaurants**, **menus**, and **food catalog** data into a single analytics experience. It supports filtering by date range, city, and currency, and surfaces insights across six modules—from an executive summary to RFM-based lifecycle segmentation.

The UI follows a dark, SaaS-inspired design system (glassmorphism KPI cards, structured sections, interactive Plotly charts) so stakeholders can explore data without writing SQL.

---

## Features

| Module | What you can explore |
|--------|----------------------|
| **Executive Dashboard** | Hero summary, revenue/customer growth, repeat rate, top city, core KPIs, revenue & order trends |
| **Customer Analytics** | Top customers by revenue, orders-per-customer distribution, repeat vs one-time buyers, segmentation (occupation, gender, income) |
| **Restaurant Analytics** | Top partners by revenue and orders, Pareto concentration curve, city-level performance scatter |
| **Food Analytics** | Most ordered and highest-revenue items (attributed model), category mix (Veg / Non-veg) |
| **RFM Analysis** | Lifecycle segments with counts, revenue share, segment charts, top customers per segment |
| **Business Insights** | 10+ auto-generated, data-driven recommendations with supporting trend chart |

**Cross-cutting capabilities**

- Sidebar filters: date range, city, currency  
- Cached data loading for faster reruns  
- Responsive KPI and insight card layout  
- Interactive Plotly visualizations with unified dark theme  

---

## KPIs Tracked

| KPI | Definition |
|-----|------------|
| **Total Revenue** | Sum of `sales_amount` for filtered orders (non-negative) |
| **Total Orders** | Count of order records in the selected period |
| **Total Customers** | Distinct `user_id` with at least one order |
| **Average Order Value (AOV)** | Total revenue ÷ total orders |
| **Revenue Growth** | Month-over-month % change in monthly revenue |
| **Customer Growth** | Month-over-month % change in active customers |
| **Repeat Purchase Rate** | % of customers with more than one order |
| **Top Performing City** | City with highest aggregated revenue |
| **Restaurant concentration** | Cumulative revenue share (Pareto / 80% line) |
| **Attributed item demand** | Menu items weighted by restaurant order volume (price-share proxy) |

---

## RFM Segmentation

Customers are scored on **Recency**, **Frequency**, and **Monetary** value using quintile-based ranks on the filtered order history:

| Score | Meaning |
|-------|---------|
| **R** | Days since last order (lower recency days → higher R score) |
| **F** | Number of distinct orders |
| **M** | Total spend in the period |

**Segments**

| Segment | Logic (simplified) |
|---------|-------------------|
| **Champions** | High R, F, and M |
| **Loyal Customers** | Strong recency and frequency |
| **Potential Loyalists** | Default mid-tier segment |
| **Big Spenders** | High monetary, moderate recency/frequency |
| **At Risk Customers** | Low recency, historically frequent |
| **Lost Customers** | Low recency and low frequency |

Each segment card shows **customer count**, **% of base**, **revenue**, **revenue share**, and a contribution bar—supporting retention, loyalty, and win-back prioritization.

---

## Business Insights

The **Business Insights** page programmatically generates recommendations from the filtered dataset, including:

- Platform GMV, order volume, and AOV snapshot  
- Month-over-month revenue movement  
- Repeat purchase rate  
- Top city and partner concentration  
- Rating vs basket size patterns  
- Category and top-item performance  
- At-risk and lost customer counts  
- Peak day-of-week demand  
- Median revenue per unit (promo ROI guardrail)  

Insights are rendered as scannable cards with highlighted priority items and a dual-axis chart (monthly revenue vs orders) for validation.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9+ |
| **App framework** | [Streamlit](https://streamlit.io/) |
| **Data manipulation** | [Pandas](https://pandas.pydata.org/) |
| **Visualization** | [Plotly](https://plotly.com/python/) (Express & Graph Objects) |
| **Styling** | Custom CSS (dark theme, glassmorphism components) |

---

## Dataset Description

All data lives in the `/data` folder as CSV files.

### Entity relationship (logical model)

```
users (user_id)
   ↑
   └── orders (order_id, user_id, r_id, order_date, sales_qty, sales_amount, currency)

restaurant (id, name, city, rating, cuisine, …)
   ↑                    ↑
   ├── orders.r_id      └── menu.r_id

food (f_id, item, veg_or_non_veg)
   ↑
   └── menu (menu_id, r_id, f_id, cuisine, price)
```

### Tables

| File | Rows (approx.) | Description |
|------|----------------|-------------|
| `users.csv` | 100,000 | Customer profiles: demographics, income band, occupation |
| `restaurant.csv` | 148,000+ | Partner listings: city, rating, cuisine, cost band, Swiggy-style metadata |
| `orders.csv` | 150,000+ | Transactions: date, quantity, amount, currency, user, restaurant |
| `menu.csv` | 1.1M+ | Restaurant–item bridge with price and cuisine |
| `food.csv` | 371,000+ | Catalog items with Veg / Non-veg classification |

### Notes for analysts

- **Primary key candidates:** `user_id`, `restaurant.id`, `food.f_id`, composite `(menu_id, r_id, f_id)` on menu  
- **Fact table:** `orders` — joins to users and restaurants for most metrics  
- **Food metrics:** Orders lack line-item `f_id`; item performance uses a **price-share attribution** model at the restaurant level  
- **Currency:** Predominantly INR; filter supports multi-currency rows where present  

---

## How to Run

### 1. Clone or download the project

```bash
cd Zomato-product-analytics
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

Open the URL shown in the terminal (default: **http://localhost:8501**).

### 5. Use the app

1. Select a page from the sidebar (Executive, Customer, Restaurant, Food, RFM, Insights).  
2. Adjust **date range**, **city**, and **currency** filters.  
3. Explore KPIs and charts; drill into RFM segment tables on the RFM page.  

---



## Project Structure

```
Zomato-product-analytics/
├── app.py              # Streamlit application (UI + analytics logic)
├── requirements.txt    # Python dependencies
├── data/
│   ├── users.csv
│   ├── restaurant.csv
│   ├── orders.csv
│   ├── menu.csv
│   └── food.csv
└── README.md
```
