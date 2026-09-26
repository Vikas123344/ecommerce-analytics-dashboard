import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask_caching import Cache

from components.navbar import create_navbar
from utils.data_loader import RAW_DF, filter_data
from pages import sales_overview, product_analytics, customer_analytics, geography_analytics

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)
app.title = "E-Commerce Analytics Dashboard"

# Caching Configuration
cache = Cache(app.server, config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
})

categories = ['All'] + list(RAW_DF['category'].unique())
countries = ['All'] + list(RAW_DF['country'].unique())

app.layout = html.Div([
    # Page Router Location
    dcc.Location(id='url', refresh=False),
    
    # Global In-Memory Data Store
    dcc.Store(id='global-store', storage_type='memory'),

    # Navbar
    create_navbar(),

    # Control Bar / Filters Section
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

        # Dynamic Content Container
        html.Div(id='page-content')
    ], fluid=True, className="px-4")
])

# Callback 1: Data Filtering & Caching into dcc.Store
@callback(
    Output('global-store', 'data'),
    [Input('dropdown-category', 'value'),
     Input('dropdown-country', 'value')]
)
@cache.memoize()
def update_store(selected_category, selected_country):
    filtered_df = filter_data(RAW_DF, selected_category, selected_country)
    return filtered_df.to_dict('records')

# Callback 2: Multi-Page Router
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
    app.run(debug=True, port=8050)