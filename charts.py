import pandas as pd
import plotly.express as px


COLOR_SEQUENCE = ["#1D4ED8", "#0F766E", "#F59E0B", "#DC2626", "#7C3AED"]
PLOT_BG = "#FFFFFF"
PAPER_BG = "#F8FAFC"


def _empty_figure(title: str):
    fig = px.scatter(title=title)
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "No data available for the current filters",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 16, "color": "#64748B"},
            }
        ],
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def _base_layout(fig, title: str):
    fig.update_layout(
        title=title,
        template="plotly_white",
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
    )
    return fig


def sales_over_time(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("Monthly Sales Trend")

    monthly_sales = (
        df.groupby("Month Sort", as_index=False)["Sales"]
        .sum()
        .sort_values("Month Sort")
    )
    monthly_sales["Month-Year"] = monthly_sales["Month Sort"].dt.strftime("%b-%Y")

    fig = px.line(
        monthly_sales,
        x="Month Sort",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend",
        color_discrete_sequence=[COLOR_SEQUENCE[0]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_xaxes(title=None, tickformat="%b\n%Y")
    fig.update_yaxes(title="Sales")
    return _base_layout(fig, "Monthly Sales Trend")


def profit_by_category(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("Profit by Category")

    category_profit = (
        df.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="Profit")
    return _base_layout(fig, "Profit by Category")


def top_10_states(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("Top 10 States by Sales")

    state_sales = (
        df.groupby("State", as_index=False)["Sales"]
        .sum()
        .nlargest(10, "Sales")
        .sort_values("Sales", ascending=True)
    )

    fig = px.bar(
        state_sales,
        x="Sales",
        y="State",
        orientation="h",
        title="Top 10 States by Sales",
        color="Sales",
        color_continuous_scale="Blues",
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(title="Sales")
    fig.update_yaxes(title=None)
    return _base_layout(fig, "Top 10 States by Sales")


def segment_pie(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("Sales by Segment")

    segment_sales = df.groupby("Segment", as_index=False)["Sales"].sum()

    fig = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.45,
        title="Sales by Segment",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(textinfo="percent+label")
    return _base_layout(fig, "Sales by Segment")


def discount_vs_profit(df: pd.DataFrame):
    if df.empty:
        return _empty_figure("Discount vs Profit")

    fig = px.scatter(
        df,
        x="Discount",
        y="Profit",
        color="Category",
        size="Sales",
        hover_data={
            "Product Name": True,
            "State": True,
            "Sales": ":.2f",
            "Discount": ":.2f",
            "Profit": ":.2f",
        },
        title="Discount vs Profit",
        color_discrete_sequence=COLOR_SEQUENCE,
        opacity=0.75,
    )
    fig.update_xaxes(title="Discount")
    fig.update_yaxes(title="Profit")
    return _base_layout(fig, "Discount vs Profit")
