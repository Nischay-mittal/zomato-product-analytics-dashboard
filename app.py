"""
Zomato Product Analytics Dashboard
Premium SaaS UI · Streamlit + Plotly + Pandas
"""

from __future__ import annotations

import io
import html
import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Zomato Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data"

# Design tokens
C = {
    "bg": "#06080f",
    "surface": "rgba(15, 23, 42, 0.55)",
    "surface_hover": "rgba(30, 41, 59, 0.75)",
    "border": "rgba(148, 163, 184, 0.12)",
    "text": "#f1f5f9",
    "muted": "#94a3b8",
    "accent": "#e23744",
    "accent2": "#ff6b6b",
    "success": "#34d399",
    "warning": "#fbbf24",
    "info": "#60a5fa",
    "purple": "#a78bfa",
}
CHART_COLORS = ["#e23744", "#ff6b6b", "#f97316", "#fbbf24", "#34d399", "#60a5fa", "#a78bfa", "#f472b6"]

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    font=dict(family="Inter, system-ui, sans-serif", color=C["muted"], size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=48, r=24, t=72, b=48),
    colorway=CHART_COLORS,
    title=dict(font=dict(size=16, color=C["text"]), x=0, xanchor="left"),
    legend=dict(
        bgcolor="rgba(15,23,42,0.6)",
        bordercolor=C["border"],
        borderwidth=1,
        font=dict(color=C["muted"]),
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        bordercolor=C["border"],
        font=dict(family="Inter, sans-serif", color=C["text"]),
    ),
    xaxis=dict(
        gridcolor="rgba(148,163,184,0.08)",
        linecolor=C["border"],
        zerolinecolor="rgba(148,163,184,0.08)",
        tickfont=dict(color=C["muted"]),
        title_font=dict(color=C["muted"]),
    ),
    yaxis=dict(
        gridcolor="rgba(148,163,184,0.08)",
        linecolor=C["border"],
        zerolinecolor="rgba(148,163,184,0.08)",
        tickfont=dict(color=C["muted"]),
        title_font=dict(color=C["muted"]),
    ),
)

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg: {C['bg']};
    --surface: {C['surface']};
    --border: {C['border']};
    --text: {C['text']};
    --muted: {C['muted']};
    --accent: {C['accent']};
    --success: {C['success']};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--text);
}}

.stApp {{
    background: radial-gradient(ellipse 120% 80% at 50% -20%, rgba(226, 55, 68, 0.14), transparent 50%),
                radial-gradient(ellipse 80% 50% at 100% 50%, rgba(96, 165, 250, 0.06), transparent 40%),
                linear-gradient(180deg, #06080f 0%, #0b1020 50%, #06080f 100%) !important;
}}

.block-container {{
    padding: 1rem 2rem 2rem !important;
    max-width: 1480px !important;
}}

#MainMenu, footer, header[data-testid="stHeader"] {{
    visibility: hidden;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #070b14 0%, #0f172a 55%, #0a0e17 100%) !important;
    border-right: 1px solid var(--border) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.25rem;
}}

[data-testid="stSidebar"] [data-testid="stMarkdown"] p,
[data-testid="stSidebar"] label {{
    color: var(--muted) !important;
}}

[data-testid="stSidebar"] .stRadio > label {{
    display: none !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
    gap: 4px;
}}

[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}}

[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(226, 55, 68, 0.08) !important;
    border-color: rgba(226, 55, 68, 0.2) !important;
}}

[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio label:has(input:checked) {{
    background: linear-gradient(135deg, rgba(226,55,68,0.2), rgba(226,55,68,0.06)) !important;
    border-color: rgba(226, 55, 68, 0.35) !important;
    color: #fff !important;
}}

.filter-card {{
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
}}

.filter-card-title {{
    display: block;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted) !important;
    margin: 12px 0 6px 0 !important;
}}

[data-testid="stMarkdownContainer"] .hero,
[data-testid="stMarkdownContainer"] .kpi-grid,
[data-testid="stMarkdownContainer"] .exec-grid,
[data-testid="stMarkdownContainer"] .insight-grid,
[data-testid="stMarkdownContainer"] .rfm-grid,
[data-testid="stMarkdownContainer"] .section-header,
[data-testid="stMarkdownContainer"] .divider-line {{
    margin-top: 0;
    margin-bottom: 0;
}}

.sidebar-logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}}

.sidebar-logo-icon {{
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #e23744, #ff6b6b);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    box-shadow: 0 8px 24px rgba(226, 55, 68, 0.35);
}}

.sidebar-logo-text h2 {{
    margin: 0;
    font-size: 1.05rem;
    font-weight: 800;
    color: #fff !important;
    letter-spacing: -0.02em;
}}

.sidebar-logo-text span {{
    font-size: 0.72rem;
    color: var(--muted);
    font-weight: 500;
}}

.nav-label {{
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin: 16px 0 8px 4px;
}}

.hero {{
    position: relative;
    padding: 28px 32px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(226,55,68,0.12) 0%, rgba(15,23,42,0.6) 45%, rgba(96,165,250,0.06) 100%);
    border: 1px solid var(--border);
    margin-bottom: 20px;
    overflow: hidden;
    backdrop-filter: blur(16px);
}}

.hero::before {{
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(226,55,68,0.15), transparent 70%);
    pointer-events: none;
}}

.hero-badge {{
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #fecaca;
    background: rgba(226, 55, 68, 0.2);
    border: 1px solid rgba(226, 55, 68, 0.35);
    padding: 5px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
}}

.hero h1 {{
    margin: 0 0 8px 0 !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #fff !important;
    letter-spacing: -0.03em !important;
    line-height: 1.2 !important;
    border: none !important;
    padding: 0 !important;
}}

.hero-sub {{
    margin: 0;
    font-size: 0.95rem;
    color: var(--muted);
    max-width: 720px;
    line-height: 1.6;
}}

.section-header {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin: 24px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}}

.section-title {{
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin: 0;
}}

.section-sub {{
    font-size: 0.78rem;
    color: #64748b;
    margin: 4px 0 0;
}}

.divider-line {{
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 20px 0;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 14px;
}}

@media (max-width: 1100px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

@media (max-width: 600px) {{
    .kpi-grid {{ grid-template-columns: 1fr; }}
}}

.kpi-card {{
    background: linear-gradient(145deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.06);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
}}

.kpi-card:hover {{
    transform: translateY(-3px);
    border-color: rgba(226, 55, 68, 0.35);
    box-shadow: 0 12px 40px rgba(226, 55, 68, 0.12), inset 0 1px 0 rgba(255,255,255,0.08);
}}

.kpi-card-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}}

.kpi-icon {{
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    background: rgba(226, 55, 68, 0.15);
    border: 1px solid rgba(226, 55, 68, 0.25);
}}

.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
}}

.kpi-value {{
    font-size: 1.65rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 8px;
}}

.kpi-trend {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
}}

.kpi-trend.up {{
    color: var(--success);
    background: rgba(52, 211, 153, 0.12);
}}

.kpi-trend.down {{
    color: #f87171;
    background: rgba(248, 113, 113, 0.12);
}}

.kpi-trend.neutral {{
    color: var(--muted);
    background: rgba(148, 163, 184, 0.1);
}}

.exec-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
}}

@media (max-width: 1100px) {{
    .exec-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

.exec-pill {{
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    backdrop-filter: blur(10px);
}}

.exec-pill-label {{
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
    margin-bottom: 6px;
}}

.exec-pill-value {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
}}

div[data-testid="stPlotlyChart"] {{
    background: rgba(15, 23, 42, 0.45);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 8px 4px 4px;
    backdrop-filter: blur(12px);
    margin-bottom: 8px;
}}

[data-testid="stSidebar"] [data-testid="stDateInput"],
[data-testid="stSidebar"] [data-testid="stMultiSelect"] {{
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 8px 12px;
    margin-bottom: 12px;
}}

.insight-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}}

@media (max-width: 900px) {{
    .insight-grid {{ grid-template-columns: 1fr; }}
}}

.insight-card {{
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    gap: 14px;
    transition: border-color 0.2s, transform 0.2s;
    backdrop-filter: blur(12px);
}}

.insight-card:hover {{
    border-color: rgba(226, 55, 68, 0.3);
    transform: translateX(2px);
}}

.insight-card.highlight {{
    border-color: rgba(226, 55, 68, 0.45);
    background: linear-gradient(135deg, rgba(226,55,68,0.1), rgba(15,23,42,0.5));
}}

.insight-icon {{
    flex-shrink: 0;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    background: rgba(226, 55, 68, 0.15);
}}

.insight-body strong {{
    color: #fff;
    font-weight: 600;
}}

.insight-num {{
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}}

.insight-text {{
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.55;
    margin: 0;
}}

.rfm-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 22px;
}}

@media (max-width: 1000px) {{
    .rfm-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

.rfm-card {{
    border-radius: 16px;
    padding: 18px 20px;
    border: 1px solid var(--border);
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(14px);
    transition: transform 0.2s, box-shadow 0.2s;
}}

.rfm-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}}

.rfm-card.champions {{ border-top: 3px solid #fbbf24; }}
.rfm-card.loyal {{ border-top: 3px solid #34d399; }}
.rfm-card.potential {{ border-top: 3px solid #60a5fa; }}
.rfm-card.at-risk {{ border-top: 3px solid #f97316; }}
.rfm-card.lost {{ border-top: 3px solid #94a3b8; }}
.rfm-card.big {{ border-top: 3px solid #a78bfa; }}

.rfm-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.rfm-stat-row {{
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 6px;
}}

.rfm-stat-row span:last-child {{
    color: #e2e8f0;
    font-weight: 600;
}}

.rfm-bar {{
    height: 4px;
    background: rgba(148,163,184,0.15);
    border-radius: 4px;
    margin-top: 10px;
    overflow: hidden;
}}

.rfm-bar-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #e23744, #ff6b6b);
}}

h2, h3 {{
    color: #fff !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}}

.stSelectbox > div > div {{
    background: rgba(15,23,42,0.8) !important;
    border-color: var(--border) !important;
}}
</style>
"""


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def _select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Keep only columns that exist in the frame."""
    return df[[c for c in columns if c in df.columns]]


@st.cache_data(show_spinner="Loading datasets…")
def load_datasets() -> dict[str, pd.DataFrame]:
    """Load and clean all CSV tables from /data (cached once per session)."""
    users = pd.read_csv(DATA_DIR / "users.csv", index_col=0)
    users = users.reset_index(drop=True)
    if "user_id" in users.columns:
        users["user_id"] = users["user_id"].astype(int)

    restaurant = pd.read_csv(DATA_DIR / "restaurant.csv", index_col=0)
    restaurant = restaurant.reset_index(drop=True)
    if "id" in restaurant.columns:
        restaurant["id"] = pd.to_numeric(restaurant["id"], errors="coerce").astype("Int64")
    if "rating" in restaurant.columns:
        restaurant["rating_num"] = pd.to_numeric(
            restaurant["rating"].replace("--", pd.NA), errors="coerce"
        )

    raw_orders = (DATA_DIR / "orders.csv").read_text(encoding="utf-8", errors="replace")
    raw_orders = raw_orders.replace("\r\n", "\n").replace("\r", "")
    orders = pd.read_csv(io.StringIO(raw_orders), index_col=0)
    orders = orders.reset_index()
    if "index" in orders.columns:
        orders = orders.rename(columns={"index": "order_id"})
    elif orders.columns[0] not in {"order_id", "order_date"}:
        orders = orders.rename(columns={orders.columns[0]: "order_id"})
    if "order_id" in orders.columns:
        orders["order_id"] = orders["order_id"].astype(int)
    if "order_date" in orders.columns:
        orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    if "sales_qty" in orders.columns:
        orders["sales_qty"] = pd.to_numeric(orders["sales_qty"], errors="coerce").fillna(0)
    if "sales_amount" in orders.columns:
        orders["sales_amount"] = pd.to_numeric(orders["sales_amount"], errors="coerce").fillna(0)
    if "user_id" in orders.columns:
        orders["user_id"] = pd.to_numeric(orders["user_id"], errors="coerce").astype("Int64")
    if "r_id" in orders.columns:
        orders["r_id"] = pd.to_numeric(orders["r_id"], errors="coerce").astype("Int64")
    if "currency" in orders.columns:
        orders["currency"] = orders["currency"].astype(str).str.strip().str.upper()
    orders = orders.dropna(subset=[c for c in ["order_date", "user_id"] if c in orders.columns])
    if "sales_amount" in orders.columns:
        orders = orders.loc[orders["sales_amount"] >= 0]

    menu = pd.read_csv(DATA_DIR / "menu.csv", index_col=0)
    menu = menu.reset_index(drop=True)
    menu = _select_columns(menu, ["menu_id", "r_id", "f_id", "price"])
    if "r_id" in menu.columns:
        menu["r_id"] = pd.to_numeric(menu["r_id"], errors="coerce").astype("Int64")
    if "price" in menu.columns:
        menu["price"] = pd.to_numeric(menu["price"], errors="coerce")

    food = pd.read_csv(DATA_DIR / "food.csv", index_col=0)
    food = food.reset_index(drop=True)
    food = _select_columns(food, ["f_id", "item", "veg_or_non_veg"])
    if "f_id" in food.columns:
        food["f_id"] = food["f_id"].astype(str)

    return {
        "users": users,
        "restaurant": restaurant,
        "orders": orders,
        "menu": menu,
        "food": food,
    }


@st.cache_data(show_spinner=False)
def get_filter_options() -> tuple[tuple, tuple, object, object]:
    """Cached metadata for sidebar controls (derived once from raw data)."""
    data = load_datasets()
    orders = data["orders"]
    restaurant = data["restaurant"]
    min_date = orders["order_date"].min().date()
    max_date = orders["order_date"].max().date()
    cities = tuple(sorted(restaurant["city"].dropna().unique().tolist()))
    currencies = tuple(sorted(orders["currency"].dropna().unique().tolist()))
    return cities, currencies, min_date, max_date


def apply_filters(
    orders: pd.DataFrame,
    restaurant: pd.DataFrame,
    date_range: tuple,
    cities: tuple[str, ...],
    currencies: tuple[str, ...],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filter orders and restaurants without copying the full orders table."""
    mask = pd.Series(True, index=orders.index)
    if date_range[0] and date_range[1]:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        mask &= (orders["order_date"] >= start) & (orders["order_date"] <= end)
    if currencies:
        mask &= orders["currency"].isin(currencies)
    if cities:
        valid_r = restaurant.loc[restaurant["city"].isin(cities), "id"].dropna().unique()
        mask &= orders["r_id"].isin(valid_r)
    o = orders.loc[mask]
    r_ids = pd.unique(o["r_id"].dropna())
    r = restaurant.loc[restaurant["id"].isin(r_ids)]
    return o, r


_USER_COLS = ["user_id", "name", "Gender", "Occupation", "Monthly Income"]
_REST_COLS = ["id", "name", "city", "rating", "rating_num", "cuisine", "cost"]
_USERS_RFM_COLS = ["user_id", "name"]


@st.cache_data(show_spinner="Preparing analytics…")
def build_master(orders: pd.DataFrame, restaurant: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    """Orders enriched with user and restaurant attributes."""
    ucols = [c for c in _USER_COLS if c in users.columns]
    rcols = [c for c in _REST_COLS if c in restaurant.columns]
    m = orders.merge(users[ucols], on="user_id", how="left")
    return m.merge(restaurant[rcols], left_on="r_id", right_on="id", how="left")


@st.cache_data(show_spinner=False)
def build_food_metrics(
    orders: pd.DataFrame, menu: pd.DataFrame, food: pd.DataFrame
) -> pd.DataFrame:
    """
    Attribute restaurant-level order volume to menu items by price share
    at each restaurant (proxy when line-item food IDs are absent in orders).
    """
    rest_orders = (
        orders.groupby("r_id", as_index=False)
        .agg(order_count=("order_id", "count"), revenue=("sales_amount", "sum"), units=("sales_qty", "sum"))
    )
    menu_rest = menu.merge(rest_orders, on="r_id", how="inner")
    menu_rest = menu_rest.dropna(subset=["price"])
    menu_rest = menu_rest[menu_rest["price"] > 0]
    price_sum = menu_rest.groupby("r_id")["price"].transform("sum")
    menu_rest["price_share"] = menu_rest["price"] / price_sum
    menu_rest["attrib_orders"] = menu_rest["order_count"] * menu_rest["price_share"]
    menu_rest["attrib_revenue"] = menu_rest["revenue"] * menu_rest["price_share"]
    menu_rest["attrib_units"] = menu_rest["units"] * menu_rest["price_share"]
    agg_spec = {
        "attrib_orders": ("attrib_orders", "sum"),
        "attrib_revenue": ("attrib_revenue", "sum"),
        "attrib_units": ("attrib_units", "sum"),
    }
    if "menu_id" in menu_rest.columns:
        agg_spec["listings"] = ("menu_id", "nunique")
    else:
        agg_spec["listings"] = ("f_id", "count")
    item = menu_rest.groupby("f_id", as_index=False).agg(**agg_spec)
    food_cols = [c for c in ["f_id", "item", "veg_or_non_veg"] if c in food.columns]
    item = item.merge(food[food_cols], on="f_id", how="left")
    if "veg_or_non_veg" in item.columns:
        item["category"] = item["veg_or_non_veg"].fillna("Unknown")
    else:
        item["category"] = "Unknown"
    return item


@st.cache_data(show_spinner=False)
def compute_rfm(orders: pd.DataFrame, as_of_iso: str) -> pd.DataFrame:
    """RFM scores and segments per customer."""
    as_of = pd.Timestamp(as_of_iso)
    rfm = orders.groupby("user_id", as_index=False).agg(
        last_order=("order_date", "max"),
        frequency=("order_id", "nunique"),
        monetary=("sales_amount", "sum"),
    )
    rfm["recency_days"] = (as_of - rfm["last_order"]).dt.days
    rfm["R"] = pd.qcut(rfm["recency_days"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1])
    rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["R"] = rfm["R"].astype(int)
    rfm["F"] = rfm["F"].astype(int)
    rfm["M"] = rfm["M"].astype(int)
    rfm["RFM_score"] = rfm["R"] + rfm["F"] + rfm["M"]

    def segment(row: pd.Series) -> str:
        r, f, m = int(row["R"]), int(row["F"]), int(row["M"])
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        if r >= 3 and f >= 3:
            return "Loyal Customers"
        if r <= 2 and f >= 3:
            return "At Risk Customers"
        if r <= 2 and f <= 2:
            return "Lost Customers"
        if m >= 4:
            return "Big Spenders"
        return "Potential Loyalists"

    rfm["segment"] = rfm.apply(segment, axis=1)
    return rfm


@st.cache_data(show_spinner=False)
def chart_monthly_trend(orders: pd.DataFrame) -> pd.DataFrame:
    """Cached monthly revenue and order counts for charts."""
    trend = orders.set_index("order_date").resample("MS").agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "count"),
    )
    trend = trend.reset_index()
    trend["month"] = trend["order_date"].dt.strftime("%b %Y")
    return trend


@st.cache_data(show_spinner=False)
def chart_customer_agg(orders: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    """Cached per-customer order and revenue aggregates."""
    cust = orders.groupby("user_id", as_index=False).agg(
        orders=("order_id", "count"),
        revenue=("sales_amount", "sum"),
    )
    ucols = [c for c in _USER_COLS if c in users.columns]
    return cust.merge(users[ucols], on="user_id", how="left")


@st.cache_data(show_spinner=False)
def chart_restaurant_agg(orders: pd.DataFrame, restaurant: pd.DataFrame) -> pd.DataFrame:
    """Cached per-restaurant performance table."""
    rest = orders.groupby("r_id", as_index=False).agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "count"),
    )
    rcols = [c for c in ["id", "name", "city", "rating"] if c in restaurant.columns]
    return rest.merge(restaurant[rcols], left_on="r_id", right_on="id", how="left")


@st.cache_data(show_spinner=False)
def chart_city_agg(master: pd.DataFrame) -> pd.DataFrame:
    """Cached city-level revenue and orders."""
    city = master.groupby("city", as_index=False).agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "count"),
    )
    return city.nlargest(20, "revenue")


@st.cache_data(show_spinner=False)
def chart_food_category_agg(food_metrics: pd.DataFrame) -> pd.DataFrame:
    """Cached category-level attributed metrics."""
    return food_metrics.groupby("category", as_index=False).agg(
        revenue=("attrib_revenue", "sum"),
        orders=("attrib_orders", "sum"),
    )


def mom_growth(series: pd.Series) -> float | None:
    if len(series) < 2 or series.iloc[-2] == 0:
        return None
    return (series.iloc[-1] - series.iloc[-2]) / series.iloc[-2] * 100


@st.cache_data(show_spinner=False)
def compute_growth_metrics(orders: pd.DataFrame) -> tuple[float | None, float | None, float]:
    """Cached MoM revenue, MoM customers, and repeat purchase rate."""
    monthly_rev = orders.set_index("order_date").resample("MS")["sales_amount"].sum()
    monthly_users = orders.set_index("order_date").resample("MS")["user_id"].nunique()
    rev_growth = mom_growth(monthly_rev)
    cust_growth = mom_growth(monthly_users)
    repeat_rate = (orders.groupby("user_id").size() > 1).mean() * 100
    return rev_growth, cust_growth, repeat_rate


@st.cache_data(show_spinner=False)
def prepare_analytics(
    date_start: str,
    date_end: str,
    cities: tuple[str, ...],
    currencies: tuple[str, ...],
) -> dict:
    """Single cached pipeline: filter → joins → RFM → chart-ready aggregates."""
    data = load_datasets()
    dr = (pd.Timestamp(date_start).date(), pd.Timestamp(date_end).date())
    orders, restaurant_f = apply_filters(data["orders"], data["restaurant"], dr, cities, currencies)
    master = build_master(orders, data["restaurant"], data["users"])
    food_metrics = build_food_metrics(orders, data["menu"], data["food"])
    as_of = pd.Timestamp(date_end)
    rfm = compute_rfm(orders, as_of.isoformat())
    rfm = rfm.merge(data["users"][_USERS_RFM_COLS], on="user_id", how="left")
    rev_growth, cust_growth, repeat_rate = compute_growth_metrics(orders)
    return {
        "orders": orders,
        "restaurant_f": restaurant_f,
        "master": master,
        "food_metrics": food_metrics,
        "rfm": rfm,
        "rev_growth": rev_growth,
        "cust_growth": cust_growth,
        "repeat_rate": repeat_rate,
        "monthly_trend": chart_monthly_trend(orders),
        "customer_agg": chart_customer_agg(orders, data["users"]),
        "restaurant_agg": chart_restaurant_agg(orders, restaurant_f),
        "city_agg": chart_city_agg(master),
        "food_category_agg": chart_food_category_agg(food_metrics),
    }


@st.cache_data(show_spinner=False)
def generate_insights(
    orders: pd.DataFrame,
    master: pd.DataFrame,
    restaurant: pd.DataFrame,
    food_metrics: pd.DataFrame,
    rfm: pd.DataFrame,
) -> list[str]:
    """Programmatic business insights (≥10) from filtered data."""
    insights: list[str] = []
    total_rev = orders["sales_amount"].sum()
    total_ord = len(orders)
    customers = orders["user_id"].nunique()
    aov = total_rev / total_ord if total_ord else 0

    insights.append(
        f"Platform generated **₹{total_rev:,.0f}** across **{total_ord:,}** orders "
        f"from **{customers:,}** active customers (AOV **₹{aov:,.0f}**)."
    )

    monthly = orders.set_index("order_date").resample("MS")["sales_amount"].sum()
    if len(monthly) >= 2:
        growth = (monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2] * 100
        insights.append(
            f"Month-over-month revenue moved **{growth:+.1f}%** "
            f"(latest month ₹{monthly.iloc[-1]:,.0f})."
        )

    repeat_rate = (orders.groupby("user_id").size() > 1).mean() * 100
    insights.append(f"**{repeat_rate:.1f}%** of customers placed more than one order (repeat rate).")

    top_city = (
        master.groupby("city")["sales_amount"].sum().sort_values(ascending=False).head(1)
    )
    if len(top_city):
        insights.append(
            f"**{top_city.index[0]}** leads cities with **₹{top_city.iloc[0]:,.0f}** revenue — "
            "prioritize supply and promos here."
        )

    rest_rev = orders.groupby("r_id")["sales_amount"].sum().sort_values(ascending=False)
    if len(rest_rev) >= 10:
        top10_share = rest_rev.head(10).sum() / rest_rev.sum() * 100
        insights.append(
            f"Top 10 restaurants contribute **{top10_share:.1f}%** of revenue — "
            "high partner concentration risk."
        )

    if "rating_num" in master.columns:
        rated = master.dropna(subset=["rating_num"])
        if len(rated) > 50:
            hi = rated[rated["rating_num"] >= 4]["sales_amount"].mean()
            lo = rated[rated["rating_num"] < 4]["sales_amount"].mean()
            insights.append(
                f"Orders at 4★+ restaurants average **₹{hi:,.0f}** vs **₹{lo:,.0f}** below 4★ — "
                "quality drives basket size."
            )

    veg_rev = food_metrics.groupby("category")["attrib_revenue"].sum()
    if len(veg_rev) >= 2:
        top_cat = veg_rev.idxmax()
        insights.append(
            f"**{top_cat}** items drive the highest attributed revenue — "
            "tailor homepage collections accordingly."
        )

    top_food = food_metrics.nlargest(1, "attrib_revenue")
    if len(top_food):
        insights.append(
            f"Top attributed item: **{top_food.iloc[0]['item']}** "
            f"(~₹{top_food.iloc[0]['attrib_revenue']:,.0f})."
        )

    seg_counts = rfm["segment"].value_counts()
    if "At Risk Customers" in seg_counts.index:
        at_risk = seg_counts["At Risk Customers"]
        insights.append(
            f"**{at_risk:,}** customers are **At Risk** — run win-back offers within 14 days."
        )
    if "Lost Customers" in seg_counts.index:
        insights.append(
            f"**{seg_counts.get('Lost Customers', 0):,}** **Lost** customers need reactivation campaigns."
        )
    if "Champions" in seg_counts.index:
        insights.append(
            f"**{seg_counts.get('Champions', 0):,}** **Champions** qualify for Gold / Pro loyalty perks."
        )

    income_col = "Monthly Income"
    if income_col in master.columns:
        inc = master.groupby(income_col)["sales_amount"].sum().sort_values(ascending=False).head(1)
        if len(inc):
            insights.append(
                f"Highest-spend income band: **{inc.index[0]}** (₹{inc.iloc[0]:,.0f}) — "
                "target ads and coupons to this cohort."
            )

    peak_dow = orders.groupby(orders["order_date"].dt.day_name())["order_id"].count()
    peak_dow = peak_dow.reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ).dropna()
    if len(peak_dow):
        insights.append(
            f"Peak order day: **{peak_dow.idxmax()}** ({peak_dow.max():,} orders) — "
            "staff delivery partners accordingly."
        )

    neg_margin = (orders["sales_amount"] / orders["sales_qty"].replace(0, pd.NA)).median()
    insights.append(
        f"Median revenue per unit sold: **₹{neg_margin:,.0f}** — "
        "use for promo ROI guardrails."
    )

    return insights[: max(10, len(insights))]


# ---------------------------------------------------------------------------
# UI helpers (presentation only)
# ---------------------------------------------------------------------------
def render_html(content: str, *, sidebar: bool = False) -> None:
    """Render HTML in one block (avoids markdown code-fence from indented multiline strings)."""
    fn = st.sidebar.markdown if sidebar else st.markdown
    fn(content.strip(), unsafe_allow_html=True)


st.markdown(CUSTOM_CSS.strip(), unsafe_allow_html=True)


def md_to_html(text: str) -> str:
    """Convert **bold** markdown in insight strings to HTML."""
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def trend_html(pct: float | None, suffix: str = "vs prior period") -> str:
    if pct is None:
        return '<span class="kpi-trend neutral">— stable</span>'
    if pct > 0:
        return f'<span class="kpi-trend up">▲ {pct:+.1f}%</span> <span style="color:#64748b;font-size:0.72rem;">{suffix}</span>'
    if pct < 0:
        return f'<span class="kpi-trend down">▼ {pct:+.1f}%</span> <span style="color:#64748b;font-size:0.72rem;">{suffix}</span>'
    return '<span class="kpi-trend neutral">— 0.0%</span>'


def hero_section(title: str, subtitle: str, badge: str = "Live Analytics") -> None:
    render_html(
        f'<div class="hero"><span class="hero-badge">{html.escape(badge)}</span>'
        f"<h1>{html.escape(title)}</h1>"
        f'<p class="hero-sub">{html.escape(subtitle)}</p></div>'
    )


def section_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="section-sub">{html.escape(subtitle)}</p>' if subtitle else ""
    render_html(
        f'<div class="section-header"><div>'
        f'<p class="section-title">{html.escape(title)}</p>{sub}'
        f"</div></div>"
    )


def divider() -> None:
    render_html('<div class="divider-line"></div>')


def kpi_cards(cards: list[dict]) -> None:
    """Glassmorphism KPI cards: label, value, icon, trend_pct."""
    parts = ['<div class="kpi-grid">']
    for c in cards:
        icon = c.get("icon", "📊")
        trend = trend_html(c.get("trend_pct"), c.get("trend_label", "vs prior period"))
        parts.append(
            f'<div class="kpi-card"><div class="kpi-card-top">'
            f'<span class="kpi-label">{html.escape(c["label"])}</span>'
            f'<span class="kpi-icon">{icon}</span></div>'
            f'<div class="kpi-value">{html.escape(str(c["value"]))}</div>{trend}</div>'
        )
    parts.append("</div>")
    render_html("".join(parts))


def exec_summary_row(items: list[tuple[str, str]]) -> None:
    pills = ['<div class="exec-grid">']
    for label, value in items:
        pills.append(
            f'<div class="exec-pill"><div class="exec-pill-label">{html.escape(label)}</div>'
            f'<div class="exec-pill-value">{html.escape(value)}</div></div>'
        )
    pills.append("</div>")
    render_html("".join(pills))


def chart_panel(fig: go.Figure, height: int = 400) -> None:
    styled_plot(fig, height)


def apply_chart_style(fig: go.Figure, title: str, subtitle: str = "") -> go.Figure:
    if subtitle:
        full_title = f"{title}<br><sup style='color:#94a3b8;font-size:11px'>{subtitle}</sup>"
    else:
        full_title = title
    fig.update_layout(
        title=dict(text=full_title, x=0.02, xanchor="left"),
        hovermode="x unified",
    )
    if fig.data and hasattr(fig.data[0], "x"):
        fig.update_traces(hovertemplate="<b>%{fullData.name}</b><br>%{x}: %{y:,.0f}<extra></extra>")
    return fig


def styled_plot(fig: go.Figure, height: int = 420) -> None:
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def insight_cards(insights: list[str]) -> None:
    icons = ["💡", "📈", "🎯", "⚡", "🔔", "🏆", "📍", "🍽️", "👥", "💰", "📊", "🚀"]
    highlight_idx = {0, 2, 5, 8}
    cards = ['<div class="insight-grid">']
    for i, text in enumerate(insights):
        hl = " highlight" if i in highlight_idx else ""
        icon = icons[i % len(icons)]
        cards.append(
            f'<div class="insight-card{hl}"><div class="insight-icon">{icon}</div>'
            f'<div class="insight-body"><div class="insight-num">Insight {i + 1}</div>'
            f'<p class="insight-text">{md_to_html(text)}</p></div></div>'
        )
    cards.append("</div>")
    render_html("".join(cards))


def rfm_segment_cards(rfm: pd.DataFrame) -> None:
    meta = {
        "Champions": ("🏆", "champions"),
        "Loyal Customers": ("💚", "loyal"),
        "Potential Loyalists": ("🌱", "potential"),
        "Big Spenders": ("💎", "big"),
        "At Risk Customers": ("⚠️", "at-risk"),
        "Lost Customers": ("💤", "lost"),
    }
    seg_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "Big Spenders",
        "At Risk Customers",
        "Lost Customers",
    ]
    total_cust = len(rfm)
    total_rev = rfm["monetary"].sum()
    stats = (
        rfm.groupby("segment")
        .agg(customers=("user_id", "count"), revenue=("monetary", "sum"))
        .reindex([s for s in seg_order if s in rfm["segment"].unique()])
    )
    cards = ['<div class="rfm-grid">']
    for seg in stats.index.dropna():
        row = stats.loc[seg]
        icon, css = meta.get(seg, ("📌", ""))
        pct_c = (row["customers"] / total_cust * 100) if total_cust else 0
        pct_r = (row["revenue"] / total_rev * 100) if total_rev else 0
        cards.append(
            f'<div class="rfm-card {css}"><div class="rfm-title">{icon} {html.escape(seg)}</div>'
            f'<div class="rfm-stat-row"><span>Customers</span><span>{int(row["customers"]):,}</span></div>'
            f'<div class="rfm-stat-row"><span>% of base</span><span>{pct_c:.1f}%</span></div>'
            f'<div class="rfm-stat-row"><span>Revenue</span><span>₹{row["revenue"]:,.0f}</span></div>'
            f'<div class="rfm-stat-row"><span>Revenue share</span><span>{pct_r:.1f}%</span></div>'
            f'<div class="rfm-bar"><div class="rfm-bar-fill" style="width:{min(pct_r, 100):.0f}%"></div></div></div>'
        )
    cards.append("</div>")
    render_html("".join(cards))


def top_city_label(master: pd.DataFrame) -> str:
    top = master.groupby("city")["sales_amount"].sum().sort_values(ascending=False).head(1)
    if len(top):
        return f"{top.index[0]} · ₹{top.iloc[0]:,.0f}"
    return "—"


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
city_options, currency_options, min_date, max_date = get_filter_options()

render_html(
    '<div class="sidebar-logo"><div class="sidebar-logo-icon">🍽️</div>'
    '<div class="sidebar-logo-text"><h2>Zomato Analytics</h2>'
    "<span>Product Intelligence</span></div></div>"
    '<p class="nav-label">Navigation</p>',
    sidebar=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Customer Analytics",
        "Restaurant Analytics",
        "Food Analytics",
        "RFM Analysis",
        "Business Insights",
    ],
    label_visibility="collapsed",
)

render_html('<p class="nav-label">Filters</p>', sidebar=True)
render_html('<p class="filter-card-title">Date range</p>', sidebar=True)
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    label_visibility="collapsed",
)
render_html('<p class="filter-card-title">Geography</p>', sidebar=True)
selected_cities = st.sidebar.multiselect("City", options=list(city_options), default=[], label_visibility="collapsed")
render_html('<p class="filter-card-title">Currency</p>', sidebar=True)
selected_currencies = st.sidebar.multiselect(
    "Currency", options=list(currency_options), default=list(currency_options), label_visibility="collapsed"
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    dr = date_range
else:
    dr = (min_date, max_date)

_cities_key = tuple(sorted(selected_cities))
_currencies_key = tuple(sorted(selected_currencies))
_analytics = prepare_analytics(
    pd.Timestamp(dr[0]).isoformat(),
    pd.Timestamp(dr[1]).isoformat(),
    _cities_key,
    _currencies_key,
)
orders = _analytics["orders"]
restaurant_f = _analytics["restaurant_f"]
master = _analytics["master"]
food_metrics = _analytics["food_metrics"]
rfm = _analytics["rfm"]
rev_growth = _analytics["rev_growth"]
cust_growth = _analytics["cust_growth"]
repeat_rate = _analytics["repeat_rate"]

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
if page == "Executive Dashboard":
    hero_section(
        "Executive Dashboard",
        "Real-time view of marketplace health — revenue, demand, and customer momentum "
        "to guide weekly business reviews and growth investments.",
        "Executive Overview",
    )

    _top_city = top_city_label(master)
    _top_city_name = _top_city.split(" · ")[0] if " · " in _top_city else _top_city

    exec_summary_row(
        [
            ("Revenue Growth", f"{rev_growth:+.1f}%" if rev_growth is not None else "—"),
            ("Customer Growth", f"{cust_growth:+.1f}%" if cust_growth is not None else "—"),
            ("Repeat Purchase Rate", f"{repeat_rate:.1f}%"),
            ("Top Performing City", _top_city_name),
        ]
    )

    total_rev = orders["sales_amount"].sum()
    total_orders = len(orders)
    total_customers = orders["user_id"].nunique()
    aov = total_rev / total_orders if total_orders else 0
    monthly_ord = _analytics["monthly_trend"]["orders"]

    section_header("Key performance indicators", "Headline metrics for the selected period")
    kpi_cards(
        [
            {"label": "Total Revenue", "value": f"₹{total_rev:,.0f}", "icon": "💰", "trend_pct": rev_growth},
            {"label": "Total Orders", "value": f"{total_orders:,}", "icon": "📦", "trend_pct": mom_growth(monthly_ord)},
            {"label": "Total Customers", "value": f"{total_customers:,}", "icon": "👥", "trend_pct": cust_growth},
            {"label": "Avg Order Value", "value": f"₹{aov:,.0f}", "icon": "🧾", "trend_pct": None},
        ]
    )

    divider()
    section_header("Performance trends", "Monthly revenue and order volume")

    trend = _analytics["monthly_trend"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(
            trend,
            x="month",
            y="revenue",
            labels={"revenue": "Revenue (₹)", "month": ""},
        )
        fig.update_traces(
            line_color=C["accent"],
            fillcolor="rgba(226, 55, 68, 0.18)",
            hovertemplate="%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )
        apply_chart_style(fig, "Revenue Trend", "Cumulative monthly GMV")
        chart_panel(fig)

    with c2:
        fig2 = px.bar(trend, x="month", y="orders", labels={"orders": "Orders", "month": ""})
        fig2.update_traces(marker_color=C["info"], hovertemplate="%{x}<br>Orders: %{y:,}<extra></extra>")
        apply_chart_style(fig2, "Order Volume Trend", "Transactions per month")
        chart_panel(fig2)

elif page == "Customer Analytics":
    hero_section(
        "Customer Analytics",
        "Understand who your highest-value users are, how often they return, and which "
        "demographic segments drive the most GMV.",
        "Customer Intelligence",
    )

    cust = _analytics["customer_agg"]

    section_header("Customer value", "Top contributors by revenue")
    top = cust.nlargest(15, "revenue")
    fig = px.bar(
        top,
        x="revenue",
        y="name",
        orientation="h",
        labels={"revenue": "Revenue (₹)", "name": "Customer"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(marker_color=C["accent"], hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>")
    apply_chart_style(fig, "Top 15 Customers by Revenue", "Ranked by lifetime value in period")
    chart_panel(fig, 460)

    section_header("Engagement & retention", "Order frequency and repeat behavior")
    c1, c2 = st.columns(2)
    with c1:
        fig_hist = px.histogram(cust, x="orders", nbins=30, labels={"orders": "Order count"})
        fig_hist.update_traces(marker_color=C["purple"])
        apply_chart_style(fig_hist, "Orders per Customer", "Distribution of purchase frequency")
        chart_panel(fig_hist)

    with c2:
        repeat = cust.assign(type=cust["orders"].apply(lambda x: "Repeat" if x > 1 else "One-time"))
        rep = repeat["type"].value_counts().reset_index()
        rep.columns = ["type", "customers"]
        fig_pie = px.pie(rep, names="type", values="customers", hole=0.5)
        apply_chart_style(fig_pie, "Repeat vs One-time Purchases", "Share of returning buyers")
        chart_panel(fig_pie)

    section_header("Customer segmentation", "Revenue breakdown by cohort")
    seg_col = st.selectbox("Segment by", ["Occupation", "Gender", "Monthly Income"], key="cust_seg")
    seg = (
        master.groupby(seg_col)
        .agg(customers=("user_id", "nunique"), revenue=("sales_amount", "sum"), orders=("order_id", "count"))
        .reset_index()
    )
    fig_seg = px.treemap(seg, path=[seg_col], values="revenue")
    apply_chart_style(fig_seg, f"Revenue by {seg_col}", "Hierarchical segment contribution")
    chart_panel(fig_seg, 440)

elif page == "Restaurant Analytics":
    hero_section(
        "Restaurant Analytics",
        "Partner performance, concentration risk, and geographic demand — optimize "
        "supply quality and city-level investments.",
        "Partner Intelligence",
    )

    rest = _analytics["restaurant_agg"]

    section_header("Leaderboards", "Top partners by revenue and volume")
    c1, c2 = st.columns(2)
    with c1:
        top_rev = rest.nlargest(15, "revenue")
        fig = px.bar(top_rev, x="revenue", y="name", orientation="h", labels={"revenue": "₹", "name": ""})
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_traces(marker_color=C["accent"], hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>")
        apply_chart_style(fig, "Top Restaurants by Revenue", "Highest GMV partners")
        chart_panel(fig, 460)

    with c2:
        top_ord = rest.nlargest(15, "orders")
        fig2 = px.bar(top_ord, x="orders", y="name", orientation="h", labels={"orders": "Orders", "name": ""})
        fig2.update_layout(yaxis={"categoryorder": "total ascending"})
        fig2.update_traces(marker_color=C["success"], hovertemplate="%{y}<br>%{x:,} orders<extra></extra>")
        apply_chart_style(fig2, "Top Restaurants by Orders", "Highest transaction volume")
        chart_panel(fig2, 460)

    section_header("Revenue concentration", "Pareto curve — partner dependency")
    rest_sorted = rest.sort_values("revenue", ascending=False).reset_index(drop=True)
    rest_sorted["cum_share"] = rest_sorted["revenue"].cumsum() / rest_sorted["revenue"].sum() * 100
    rest_sorted["rank_pct"] = (rest_sorted.index + 1) / len(rest_sorted) * 100
    fig_p = go.Figure()
    fig_p.add_trace(
        go.Scatter(
            x=rest_sorted["rank_pct"],
            y=rest_sorted["cum_share"],
            mode="lines",
            name="Cumulative %",
            line=dict(color=C["accent"], width=3),
            hovertemplate="%{x:.0f}% of restaurants<br>%{y:.1f}% of revenue<extra></extra>",
        )
    )
    fig_p.add_hline(y=80, line_dash="dash", line_color=C["muted"], annotation_text="80% revenue")
    apply_chart_style(fig_p, "Restaurant Revenue Concentration", "% of restaurants vs cumulative GMV")
    chart_panel(fig_p)

    section_header("Geographic performance", "City-level demand map")
    city_perf = _analytics["city_agg"]
    fig_city = px.scatter(
        city_perf,
        x="orders",
        y="revenue",
        text="city",
        labels={"revenue": "Revenue (₹)", "orders": "Orders"},
        size="revenue",
        size_max=40,
    )
    fig_city.update_traces(
        marker_color=C["info"],
        textposition="top center",
        hovertemplate="<b>%{text}</b><br>Orders: %{x:,}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    )
    apply_chart_style(fig_city, "City Performance", "Orders vs revenue bubble size = GMV")
    chart_panel(fig_city)

elif page == "Food Analytics":
    hero_section(
        "Food Analytics",
        "Menu catalog performance with attributed item demand — inform merchandising, "
        "search ranking, and category campaigns.",
        "Catalog Intelligence",
    )

    fm = food_metrics.dropna(subset=["item"])

    section_header("Item performance", "Attributed orders and revenue")
    c1, c2 = st.columns(2)
    with c1:
        top_items = fm.nlargest(15, "attrib_orders")
        fig = px.bar(
            top_items,
            x="attrib_orders",
            y="item",
            orientation="h",
            labels={"attrib_orders": "Attributed orders", "item": ""},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_traces(marker_color=C["accent"], hovertemplate="%{y}<br>%{x:,.1f} orders<extra></extra>")
        apply_chart_style(fig, "Most Ordered Items (attributed)", "Price-share allocation model")
        chart_panel(fig, 460)

    with c2:
        top_rev = fm.nlargest(15, "attrib_revenue")
        fig2 = px.bar(
            top_rev,
            x="attrib_revenue",
            y="item",
            orientation="h",
            labels={"attrib_revenue": "₹", "item": ""},
        )
        fig2.update_layout(yaxis={"categoryorder": "total ascending"})
        fig2.update_traces(marker_color=C["warning"], hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>")
        apply_chart_style(fig2, "Highest Revenue Items (attributed)", "Top GMV menu items")
        chart_panel(fig2, 460)

    section_header("Category performance", "Veg / non-veg and catalog mix")
    cat = _analytics["food_category_agg"]
    c3, c4 = st.columns(2)
    with c3:
        fig_cat = px.pie(cat, names="category", values="revenue", hole=0.45, color_discrete_sequence=CHART_COLORS)
        apply_chart_style(fig_cat, "Category Revenue Share", "Attributed GMV by category")
        chart_panel(fig_cat)

    with c4:
        fig_bar = px.bar(cat, x="category", y="orders", labels={"orders": "Attributed orders"})
        fig_bar.update_traces(marker_color=C["purple"])
        apply_chart_style(fig_bar, "Category Order Volume", "Attributed order volume")
        chart_panel(fig_bar)

elif page == "RFM Analysis":
    hero_section(
        "RFM Analysis",
        "Segment customers by recency, frequency, and monetary value — prioritize retention, "
        "loyalty, and win-back programs with precision.",
        "Lifecycle Segmentation",
    )

    seg_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "Big Spenders",
        "At Risk Customers",
        "Lost Customers",
    ]
    seg_summary = (
        rfm.groupby("segment")
        .agg(customers=("user_id", "count"), avg_monetary=("monetary", "mean"), avg_frequency=("frequency", "mean"))
        .reindex([s for s in seg_order if s in rfm["segment"].unique()])
        .dropna(how="all")
    )

    section_header("Segment overview", "Counts, revenue share, and contribution")
    kpi_cards(
        [
            {
                "label": "Champions",
                "value": f"{(rfm['segment'] == 'Champions').sum():,}",
                "icon": "🏆",
                "trend_pct": None,
                "trend_label": "high-value segment",
            },
            {
                "label": "Loyal Customers",
                "value": f"{(rfm['segment'] == 'Loyal Customers').sum():,}",
                "icon": "💚",
                "trend_pct": None,
                "trend_label": "retained buyers",
            },
            {
                "label": "At Risk",
                "value": f"{(rfm['segment'] == 'At Risk Customers').sum():,}",
                "icon": "⚠️",
                "trend_pct": None,
                "trend_label": "needs win-back",
            },
            {
                "label": "Lost",
                "value": f"{(rfm['segment'] == 'Lost Customers').sum():,}",
                "icon": "💤",
                "trend_pct": None,
                "trend_label": "reactivation pool",
            },
        ]
    )

    rfm_segment_cards(rfm)
    divider()

    section_header("Segment analytics", "Distribution and RFM scatter")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            seg_summary.reset_index(),
            x="segment",
            y="customers",
            color="segment",
            color_discrete_sequence=CHART_COLORS,
        )
        fig.update_layout(showlegend=False)
        apply_chart_style(fig, "Customers by RFM Segment", "Segment population")
        chart_panel(fig)

    with c2:
        fig2 = px.scatter(
            rfm,
            x="frequency",
            y="monetary",
            color="segment",
            size="R",
            labels={"frequency": "Frequency", "monetary": "Monetary (₹)"},
            hover_data=["user_id", "name"],
            color_discrete_sequence=CHART_COLORS,
        )
        apply_chart_style(fig2, "RFM Scatter", "Frequency × monetary by segment")
        chart_panel(fig2, 440)

    section_header("Segment drill-down", "Top customers per lifecycle stage")
    for label in ["Champions", "Loyal Customers", "At Risk Customers", "Lost Customers"]:
        subset = rfm[rfm["segment"] == label].nlargest(10, "monetary")[
            ["user_id", "name", "recency_days", "frequency", "monetary", "RFM_score"]
        ]
        if len(subset):
            st.markdown(f"#### {label}")
            st.dataframe(subset, use_container_width=True, hide_index=True)

else:
    hero_section(
        "Business Insights",
        "Actionable recommendations synthesized from marketplace data — ready for "
        "product, growth, and operations leadership.",
        "Strategic Recommendations",
    )

    insights = generate_insights(orders, master, restaurant_f, food_metrics, rfm)
    section_header("Priority insights", f"{len(insights)} data-driven recommendations")
    insight_cards(insights)

    divider()
    section_header("Supporting evidence", "Monthly revenue vs orders")
    trend = _analytics["monthly_trend"]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=trend["order_date"],
            y=trend["orders"],
            name="Orders",
            yaxis="y2",
            opacity=0.4,
            marker_color=C["info"],
            hovertemplate="%{x|%b %Y}<br>Orders: %{y:,}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=trend["order_date"],
            y=trend["revenue"],
            name="Revenue",
            line=dict(color=C["accent"], width=3),
            hovertemplate="%{x|%b %Y}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        yaxis=dict(title="Revenue (₹)"),
        yaxis2=dict(title="Orders", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    apply_chart_style(fig, "Monthly Revenue & Orders", "Dual-axis trend validation")
    chart_panel(fig)
