import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from fuelproject_tables import dfgen

city_list = dfgen.city_overall()["Municipio"].unique()

@callback(
        Output(),
        Input()
)
def chart(referred_chart):
    city_list_dropdown= dcc.Dropdown(
        id=referred_chart,
        children=[city_list],
        multi=True
    )
    return city_list_dropdown

