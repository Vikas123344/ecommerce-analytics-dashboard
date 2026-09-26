from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def layout():
    return html.Div([
        html.H3("Geography Analytics", className="page-title"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Global Interactive Sales Map"),
                    dcc.Graph(id="chart-geo-map")
                ], className="graph-card shadow-sm p-3 mb-4")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Sales By Country"),
                    dcc.Graph(id="chart-sales-country")
                ], className="graph-card shadow-sm p-3")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H5("Sales By State"),
                    dcc.Graph(id="chart-sales-state")
                ], className="graph-card shadow-sm p-3")
            ], width=6)
        ])
    ])

@callback(
    [Output("chart-geo-map", "figure"),
     Output("chart-sales-country", "figure"),
     Output("chart-sales-state", "figure")],
    [Input("global-store", "data")]
)
def update_geo_analytics(store_data):
    df = pd.DataFrame(store_data)
    if df.empty:
        return {}, {}, {}

    country_df = df.groupby('country')['revenue'].sum().reset_index()
    state_df = df.groupby(['state', 'country'])['revenue'].sum().reset_index()

    fig_map = px.choropleth(
        country_df,
        locations="country",
        locationmode="country names",
        color="revenue",
        color_continuous_scale="Viridis",
        template="plotly_white"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig_country = px.bar(country_df, x='country', y='revenue', color='revenue', template="plotly_white")
    fig_state = px.bar(state_df.sort_values(by='revenue', ascending=False).head(10), x='state', y='revenue', color='country', template="plotly_white")

    return fig_map, fig_country, fig_state