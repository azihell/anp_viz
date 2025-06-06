from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from fuelproject_tables import dfgen

cities = dfgen.city_overall()["Municipio"].unique().tolist()

def chart(referred_chart):
    city_dropdown_list = dbc.Container([
        dcc.Dropdown(
            id = referred_chart,
            options = cities,
            value=["Feira De Santana", "Salvador"],
            multi=True
        ),
    ])
    return city_dropdown_list