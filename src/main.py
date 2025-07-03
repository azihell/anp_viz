import os
import sys

# import src.app_plots

# Get the path to the directory *containing* src (your repository root)
# This allows Python to find 'src' as a package when you run main.py directly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from dash import Dash, dcc #, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import src.app_components, src.app_plots


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
load_figure_template("SLATE")
theme = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[theme, dbc_css, dbc.icons.FONT_AWESOME])
server = app.server

# Top navigation bar object creation:
navbar_class = src.app_components.MyNavbar("top_bar", None)
navbar_class.register_callbacks(app)

# Cross-filter class to ensure robustness among parameters available to the user
filters = src.app_components.Crossfilter()
filters.register_callback(app)

# KPI that counts gas stations 
stations_kpi = src.app_components.StationsKPI("station_kpi")

# City overview table

city_overview = src.app_plots.CityOverview("city_summary_table")

app.layout = dbc.Container(children=[
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='filtered-selection',
        data={"Municipio":None, "Ano":None, "Produto":None}
        ),
    dcc.Store(id="all-possible-values",
        data={"Municipio":None, "Ano":None, "Produto":None}
              ),
    dcc.Store(id="filtered-dataset",
        data={}
              ),
    dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Alerta de seleção")),
            dbc.ModalBody(dcc.Markdown("Por favor, selecione ao menos uma cidade e um produto para que os gráficos sejam atualizados.")),
        ],
        id="bad-filtering-popup", is_open = False, size="sm", centered=True,
    ),
    # Top navigation bar render method
    navbar_class.render(),
    dbc.Container(
        # className="dbc",    # Uncomment to enable DataTable to be styled according to the theme selected. But loses "style_as_list_view" : True," property while at it.
        style={"max-width": "100%", "padding": "50px", "position":"relative", "top":"20px"},
        children = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Número de Postos"),
                        dbc.CardBody([
                            dcc.Loading(
                                id="kpi-loading",
                                type="graph",
                                children=[
                                    dcc.Graph(
                                        id = "station_kpi",
                                        config={'displayModeBar': False}
                                    ) 
                                ]
                            )
                        ]),
                        src.app_components.StationsKPI("station_kpi").register_callback(app),
                    ], color="secondary", outline=True
                ),
            ], width = 3),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card(children=[dcc.Graph(id = "fuel_avg")],
                         color="secondary", outline=True
                    )
            ], width = 6),
            # dbc.Col([
            #     dbc.Card(children=[dcc.Graph(id = "city_alltime_avg")],
            #              color="secondary", outline=True
            #         )
            # ], width = 3),
            dbc.Col([
                dbc.Card([
                    dbc.Container(id = "city_summary_table"),
                    src.app_plots.CityOverview("city_summary_table").register_callback(app),
                ], color="secondary", outline=True)
            ], width = 6),
            dbc.Col([
                dbc.Card([
                    
                ], color="secondary", outline=True)
            ], width = 6),
        ]),

        # dbc.Row([
        #     dbc.Col([

        #     ])
        # ])
    ]),
], fluid=True)

if __name__ == "__main__":
  app.run(debug=True, port=8090)