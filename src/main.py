from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import sys
# 
sys.path.append("./scripts")
sys.path.append("./scripts/fuelcomponents")
sys.path.append("./scripts/fuelproject_tables")
from fuelproject_tables import dfgen
from fuelcomponents import year_slider, all_time_avg, city_overview, navbar, offcanvas

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
load_figure_template("SLATE")
theme = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[theme, dbc_css, dbc.icons.FONT_AWESOME])

app.layout = dbc.Container(children=[
    # Top navigation bar
        navbar.generate_navbar(),
    dbc.Container(
        # className="dbc",    # Uncomment to enable DataTable to be styled according to the theme selected. But loses "style_as_list_view" : True," property while at it.
        style={"max-width": "100%", "padding": "50px", "position":"relative", "top":"20px"},
        children = [
        dbc.Row([
            dbc.Col([
                dbc.Card(children=[dcc.Graph(id = "fuel_avg")],
                         color="secondary", outline=True
                    )
            ], width = 6),
            dbc.Col([
                dbc.Card([
                    dbc.Container(id = "city_summary_over_year")    # html.Div(id="city_summary_over_year") works too
                ], color="secondary", outline=True)
            ], width = 6),
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id = "city_alltime_avg",
                    figure = px.bar(
                        dfgen.all_time_avg().sort_values("Municipio",ascending=True),
                        title = "Média normalizada por cidade",
                        x = "Municipio",
                        y = "Normalized",
                        color = "Produto",
                    )
                ),
            ])
        ])
    ])
], fluid=True)

if __name__ == "__main__":
  app.run()