from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import sys
# 
sys.path.append("./scripts")
sys.path.append("./scripts/fuelcomponents")
sys.path.append("./scripts/fuelproject_tables")
from fuelproject_tables import dfgen
from fuelcomponents import year_slider, all_time_avg, city_overview

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dcc.Markdown("## ANP retail data "),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4("Select a range in years"),
            year_slider.chart("all_time_slider"),
            dcc.Graph(
                id = "fuel_avg",
            ),
        ]),
        dbc.Col([
            html.H4("Select a range in years"),
            year_slider.chart("slider"),
            dbc.Table(id="city_summary_over_year")    # html.Div(id="cities_table") works too
        ]),
    ]),

    # dbc.Row([
    #     dbc.Col([
    #         dcc.Graph(
    #             id = "city_alltime_avg",
    #             figure = px.bar(
    #                 dfgen.all_time_avg().sort_values("Municipio",ascending=True),
    #                 title = "City all-time average, all products",
    #                 x = "Municipio",
    #                 y = "Normalized",
    #                 color = "Produto",
    #             )
    #         ),
    #     ])
    # ])
])

if __name__ == "__main__":
  app.run()