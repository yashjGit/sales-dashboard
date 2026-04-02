import pandas as pd
import streamlit as st

from charts import (
    discount_vs_profit,
    profit_by_category,
    sales_over_time,
    segment_pie,
    top_10_states,
)
from data_loader import load_data


st.set_page_config(page_title="📊 Sales Intelligence Dashboard", layout="wide")


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data()


def format_currency(value: float, symbol: str = "$") -> str:
    return f"{symbol}{value:,.2f}"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .dashboard-card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(8px);
        }
        .dashboard-card h4 {
            margin: 0;
            color: #475569;
            font-size: 0.95rem;
            font-weight: 600;
        }
        .dashboard-card h2 {
            margin: 0.35rem 0 0;
            color: #0f172a;
            font-size: 1.8rem;
            font-weight: 700;
        }
        .dashboard-card p {
            margin: 0.35rem 0 0;
            color: #64748b;
            font-size: 0.88rem;
        }
        .section-heading {
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
            color: #0f172a;
            font-weight: 700;
            font-size: 1.15rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="dashboard-card">
            <h4>{title}</h4>
            <h2>{value}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_styles()
df = get_data()

st.title("📊 Sales Intelligence Dashboard")
st.caption(
    "Track revenue, profitability, customer segments, and regional performance "
    "from the Superstore dataset in one interactive workspace."
)

st.sidebar.header("Filter Dashboard")

regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
)

categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)

min_year = int(df["Order Date"].dt.year.min())
max_year = int(df["Order Date"].dt.year.max())
selected_years = st.sidebar.slider(
    "Order Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Order Date"].dt.year.between(selected_years[0], selected_years[1])
].copy()

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_profit_margin = filtered_df["Profit Margin %"].mean() if not filtered_df.empty else 0.0

metric_cols = st.columns(4)
with metric_cols[0]:
    render_metric_card("Total Sales", format_currency(total_sales, "$"), "Revenue in current view")
with metric_cols[1]:
    render_metric_card("Total Profit", format_currency(total_profit, "$"), "Net profit across filtered orders")
with metric_cols[2]:
    render_metric_card("Total Orders", f"{total_orders:,}", "Unique orders in scope")
with metric_cols[3]:
    render_metric_card("Avg Profit Margin %", f"{avg_profit_margin:.2f}%", "Average profitability ratio")

st.markdown('<div class="section-heading">Performance Overview</div>', unsafe_allow_html=True)
chart_col_1, chart_col_2 = st.columns(2)

with chart_col_1:
    st.plotly_chart(sales_over_time(filtered_df), use_container_width=True)
    st.plotly_chart(top_10_states(filtered_df), use_container_width=True)
    st.plotly_chart(discount_vs_profit(filtered_df), use_container_width=True)

with chart_col_2:
    st.plotly_chart(profit_by_category(filtered_df), use_container_width=True)
    st.plotly_chart(segment_pie(filtered_df), use_container_width=True)

with st.expander("📋 Raw Data", expanded=False):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
