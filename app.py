import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask_caching import Cache

from components.navbar import create_navbar
from utils.data_loader import RAW_DF, filter_data
from pages import sales_overview, product_analytics, customer_analytics, geography_analytics

# Initialize Dash App
dash_app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)
dash_app.title = "E-Commerce Analytics Dashboard"

# EXPOSE FLASK SERVER FOR VERCEL
server = dash_app.server
app = server  # Vercel entry point looks for 'app'

# In-Memory Cache configuration
cache = Cache(server, config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
})

categories = ['All'] + list(RAW_DF['category'].unique())
countries = ['All'] + list(RAW_DF['country'].unique())

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='global-store', storage_type='memory'),

    create_navbar(),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Filter Category:", className="fw-bold text-muted me-2"),
                    dcc.Dropdown(
                        id='dropdown-category',
                        options=[{'label': c, 'value': c} for c in categories],
                        value='All',
                        clearable=False,
                        style={'minWidth': '200px'}
                    )
                ], className="d-flex align-items-center me-3")
            ], width="auto"),
            dbc.Col([
                html.Div([
                    html.Label("Filter Country:", className="fw-bold text-muted me-2"),
                    dcc.Dropdown(
                        id='dropdown-country',
                        options=[{'label': c, 'value': c} for c in countries],
                        value='All',
                        clearable=False,
                        style={'minWidth': '200px'}
                    )
                ], className="d-flex align-items-center")
            ], width="auto")
        ], className="filter-panel shadow-sm mb-4 ms-0 me-0 align-items-center"),

        html.Div(id='page-content')
    ], fluid=True, className="px-4")
])

@callback(
    Output('global-store', 'data'),
    [Input('dropdown-category', 'value'),
     Input('dropdown-country', 'value')]
)
@cache.memoize()
def update_store(selected_category, selected_country):
    filtered_df = filter_data(RAW_DF, selected_category, selected_country)
    return filtered_df.to_dict('records')

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/product-analytics':
        return product_analytics.layout()
    elif pathname == '/customer-analytics':
        return customer_analytics.layout()
    elif pathname == '/geography-analytics':
        return geography_analytics.layout()
    else:
        return sales_overview.layout()

if __name__ == '__main__':
    dash_app.run(debug=True, port=8050)