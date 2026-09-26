from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Sales Overview", href="/")),
            dbc.NavItem(dbc.NavLink("Product Analytics", href="/product-analytics")),
            dbc.NavItem(dbc.NavLink("Customer Analytics", href="/customer-analytics")),
            dbc.NavItem(dbc.NavLink("Geography Analytics", href="/geography-analytics")),
        ],
        brand="🛒 E-Commerce Analytics",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4 shadow-sm"
    )