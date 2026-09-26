from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def layout():
    return html.Div([
        html.H3("Customer Analytics", className="page-title"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("New vs. Returning Customers"),
                    dcc.Graph(id="chart-new-vs-returning")
                ], className="graph-card shadow-sm p-3 mb-4")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H5("Customer Lifetime Value (LTV Distribution)"),
                    dcc.Graph(id="chart-clv")
                ], className="graph-card shadow-sm p-3 mb-4")
            ], width=8),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Customer Segmentation Revenue"),
                    dcc.Graph(id="chart-segmentation")
                ], className="graph-card shadow-sm p-3")
            ], width=12)
        ])
    ])

@callback(
    [Output("chart-new-vs-returning", "figure"),
     Output("chart-clv", "figure"),
     Output("chart-segmentation", "figure")],
    [Input("global-store", "data")]
)
def update_customer_analytics(store_data):
    df = pd.DataFrame(store_data)
    if df.empty:
        return {}, {}, {}

    cust_type = df.groupby('customer_type')['order_id'].nunique().reset_index()
    fig_type = px.pie(cust_type, names='customer_type', values='order_id', color_discrete_sequence=['#3b82f6', '#10b981'])

    clv_df = df.groupby('customer_id')['revenue'].sum().reset_index()
    fig_clv = px.histogram(clv_df, x='revenue', nbins=20, labels={'revenue': 'Total Spend per Customer ($)'}, template="plotly_white")

    seg_df = df.groupby(['segment', 'customer_type'])['revenue'].sum().reset_index()
    fig_seg = px.bar(seg_df, x='segment', y='revenue', color='customer_type', barmode='group', template="plotly_white")

    return fig_type, fig_clv, fig_seg