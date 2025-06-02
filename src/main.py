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
from fuelcomponents import year_slider, all_time_avg, city_overview

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
load_figure_template("SLATE")
theme = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[theme, dbc_css])

app.layout = dbc.Container(
    # className="dbc",    # Uncomment to enable DataTable to be styled according to the theme selected. But loses "style_as_list_view" : True," property while at it.
    style={'max-width': '90%', 'border': '4px ridge silver', "border-radius": "4px", 'padding': '50px'},
    children = [
    dcc.Markdown("# Histórico de preços de combustível"),
    dcc.Markdown("Baseado em *dataset* da Agência Nacional de Petróleo e Gás. [Disponível no Kaggle](https://www.kaggle.com/datasets/paulogladson/anp-combustveis) e generosamente compilado por [Paulo Gladson](https://github.com/PauloGladson)."),
    html.Br(),
    dbc.Row([
        dbc.Card([
            dbc.CardHeader("Escolha uma faixa (em anos) como filtro:"),
            dbc.CardBody([
                    year_slider.chart("main_slider")
                ])
        ], color="secondary", outline=True
         ),
        dbc.Col([
          
        dbc.Card([
            dcc.Graph(id = "fuel_avg"),
        ], color="secondary", outline=True)

        ], width = 6),
        dbc.Col([
          
        dbc.Card([
            dbc.Container(id = "city_summary_over_year")    # html.Div(id="city_summary_over_year") works too
        ], color="secondary", outline=True)

        ], width = 6),
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