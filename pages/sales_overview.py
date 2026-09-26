from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def layout():
    return html.Div([
        html.H3("Sales Overview", className="page-title"),
        
        # KPI Cards Row
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total Revenue", className="card-subtitle text-muted"),
                    html.H3(id="kpi-revenue", className="text-primary fw-bold")
                ])
            ], className="kpi-card shadow-sm"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total Orders", className="card-subtitle text-muted"),
                    html.H3(id="kpi-orders", className="text-success fw-bold")
                ])
            ], className="kpi-card shadow-sm"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total Profit", className="card-subtitle text-muted"),
                    html.H3(id="kpi-profit", className="text-info fw-bold")
                ])
            ], className="kpi-card shadow-sm"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Avg Order Value (AOV)", className="card-subtitle text-muted"),
                    html.H3(id="kpi-aov", className="text-warning fw-bold")
                ])
            ], className="kpi-card shadow-sm"), width=3),
        ], className="mb-4"),

        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Monthly Revenue Trend"),
                    dcc.Graph(id="chart-monthly-revenue")
                ], className="graph-card shadow-sm p-3")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H5("Daily Orders Flow"),
                    dcc.Graph(id="chart-daily-orders")
                ], className="graph-card shadow-sm p-3")
            ], width=6)
        ])
    ])

@callback(
    [Output("kpi-revenue", "children"),
     Output("kpi-orders", "children"),
     Output("kpi-profit", "children"),
     Output("kpi-aov", "children"),
     Output("chart-monthly-revenue", "figure"),
     Output("chart-daily-orders", "figure")],
    [Input("global-store", "data")]
)
def update_sales_overview(store_data):
    if not store_data:
        return "$0.00", "0", "$0.00", "$0.00", {}, {}

    df = pd.DataFrame(store_data)
    if df.empty:
        return "$0.00", "0", "$0.00", "$0.00", {}, {}

    # Core Metrics
    rev = df['revenue'].sum()
    orders = df['order_id'].nunique()
    profit = df['profit'].sum()
    aov = rev / orders if orders > 0 else 0

    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Monthly Aggregation using pd.Grouper (Safe & Reliable)
    monthly = (
        df.groupby(pd.Grouper(key='date', freq='ME'))['revenue']
        .sum()
        .reset_index()
    )

    # Daily Aggregation
    daily = (
        df.groupby(pd.Grouper(key='date', freq='D'))['order_id']
        .nunique()
        .reset_index()
    )

    # Figures
    fig_monthly = px.line(
        monthly, 
        x='date', 
        y='revenue', 
        markers=True, 
        template="plotly_white",
        labels={'date': 'Month', 'revenue': 'Revenue ($)'}
    )
    fig_monthly.update_traces(line_color="#2b580c")

    fig_daily = px.histogram(
        daily, 
        x='date', 
        y='order_id', 
        template="plotly_white",
        labels={'date': 'Date', 'order_id': 'Orders'}
    )
    fig_daily.update_traces(marker_color="#6366f1")

    return (
        f"${rev:,.2f}",
        f"{orders:,}",
        f"${profit:,.2f}",
        f"${aov:,.2f}",
        fig_monthly,
        fig_daily
    )