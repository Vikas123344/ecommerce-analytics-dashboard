from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def layout():
    return html.Div([
        html.H3("Product Analytics", className="page-title"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Top 5 Best Selling Products"),
                    dcc.Graph(id="chart-best-selling")
                ], className="graph-card shadow-sm p-3 mb-4")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H5("Bottom 5 Lowest Selling Products"),
                    dcc.Graph(id="chart-worst-selling")
                ], className="graph-card shadow-sm p-3 mb-4")
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Category Performance"),
                    dcc.Graph(id="chart-category-perf")
                ], className="graph-card shadow-sm p-3")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H5("Product Profitability Margin"),
                    dcc.Graph(id="chart-profitability")
                ], className="graph-card shadow-sm p-3")
            ], width=6)
        ])
    ])

@callback(
    [Output("chart-best-selling", "figure"),
     Output("chart-worst-selling", "figure"),
     Output("chart-category-perf", "figure"),
     Output("chart-profitability", "figure")],
    [Input("global-store", "data")]
)
def update_product_analytics(store_data):
    df = pd.DataFrame(store_data)
    if df.empty:
        return {}, {}, {}, {}

    prod_summary = df.groupby('product_id').agg({'revenue': 'sum', 'profit': 'sum'}).reset_index()
    
    top_5 = prod_summary.nlargest(5, 'revenue')
    bot_5 = prod_summary.nsmallest(5, 'revenue')

    fig_best = px.bar(top_5, x='revenue', y='product_id', orientation='h', template="plotly_white", color='revenue')
    fig_worst = px.bar(bot_5, x='revenue', y='product_id', orientation='h', template="plotly_white", color_discrete_sequence=['#ef4444'])

    cat_summary = df.groupby('category')[['revenue', 'profit']].sum().reset_index()
    fig_cat = px.pie(cat_summary, values='revenue', names='category', hole=0.4, template="plotly_white")

    fig_prof = px.scatter(prod_summary, x='revenue', y='profit', size='revenue', hover_name='product_id', template="plotly_white")

    return fig_best, fig_worst, fig_cat, fig_prof