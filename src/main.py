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

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])
load_figure_template("SLATE")

app.layout = dbc.Container([
    dcc.Markdown("# Histórico de preços de combustível"),
    dcc.Markdown("Baseado em *dataset* da Agência Nacional de Petróleo e Gás. [Disponível no Kaggle](https://www.kaggle.com/datasets/paulogladson/anp-combustveis) e generosamente compilado por [Paulo Gladson](https://github.com/PauloGladson)."),
    html.Br(),
    dbc.Row([
        dbc.Card([
            dbc.CardHeader("Escolha uma faixa (em anos) como filtro:"),
            dbc.CardBody([
                    # dcc.Markdown("Escolha uma faixa de anos:"),
                    year_slider.chart("main_slider")
                ])
        ], color="secondary", outline=True
         ),
        dbc.Col([
            dcc.Graph(id = "fuel_avg"),
        ], width = 6),
        dbc.Col([
            dbc.Table(id = "city_summary_over_year")    # html.Div(id="city_summary_over_year") works too
        ], width = 6, className="dbc dbc-row-selectable"),
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
], style={'max-width': '90%', 'border': '4px ridge silver', "border-radius": "4px", 'padding': '50px'})

if __name__ == "__main__":
  app.run()