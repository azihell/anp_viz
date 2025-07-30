from os import path as _os_path
from sys import path as _sys_path

# Get the path to the directory *containing* src (your repository root)
# This allows Python to find 'src' as a package when you run main.py directly
current_dir = _os_path.dirname(_os_path.abspath(__file__))
parent_dir = _os_path.dirname(current_dir)
if parent_dir not in _sys_path:
    _sys_path.insert(0, parent_dir)

from dash_extensions.enrich import DashProxy, ServersideOutputTransform, dcc
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
import src.app_components, src.app_plots

load_figure_template(["slate"])

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
theme = dbc.themes.SLATE
app = DashProxy(__name__, external_stylesheets=[theme, dbc.icons.FONT_AWESOME, dbc_css], transforms=[ServersideOutputTransform()])
server = app.server

# Top navigation bar object creation:
navbar_class = src.app_components.MyNavbar("top_bar", None)
navbar_class.register_callbacks(app)

# Cross-filter class to ensure robustness among parameters available to the user
filters = src.app_components.Crossfilter()
filters.register_callback(app)

# City overview table
city_overview = src.app_plots.CityOverview("city_summary_table")
alltime_avg = src.app_plots.AllTimeAvg("fuel_avg")
cities_avg = src.app_plots.CitiesTimeAvg("cities-avg-price")

app.layout = dbc.Container(children=[
    dcc.Store(id='store-first-load-flag', data=None),
    dcc.Store(id='filtered-selection', data={"Municipio":None, "Ano":None, "Produto":None}),
    dcc.Store(id="all-possible-values", data={"Municipio":None, "Ano":None, "Produto":None}),
    dcc.Store(id="filtered-dataset", data={}),
    dcc.Store(id='summary_table_data', data=None),
    dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Alerta de seleção")),
            dbc.ModalBody(dcc.Markdown("Por favor, selecione ao menos uma cidade e um produto para que os gráficos sejam atualizados.")),
        ],
        id="bad-filtering-popup", is_open = False, size="sm", centered=True,
    ),
    # Top navigation bar is rendered
    navbar_class.render(),

    # Row #1 - KPIs
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Variação no número de postos"),
                    dbc.CardBody(
                        children=[
                            dcc.Loading(
                                id="carregador",
                                type="default",
                                children=[
                                    dbc.Container(id="station_count")
                                ]
                            )
                        ]
                    ),
                    src.app_components.StationsKPI("station_count").register_callback(app),
                ], color="secondary", outline=True, id="stations_header"
            ),
            dbc.Tooltip("O valor na segunda linha mostra o aumento (verde) ou redução (vermelho) do número de postos do 'Ano final' em comparação ao 'Ano inicial'", target="stations_header"),
        ], width = 2),
    ], className="mb-4"),

    # Row #2 - line chart + table
    dbc.Row(
        children=[
            dbc.Col([
                dbc.Card([
                    dbc.Container(
                        dcc.Loading(
                            id="line-plot-loader",
                            type="default",
                            children=[
                                dbc.Container(
                                    dcc.Graph(id="fuel_avg"),
                                    id="fuel-avg-graph-container",
                                )
                            ]
                        ),
                    ),
                    dbc.Tooltip("Clique e arraste no gráfico para selecionar uma faixa de tempo que também funcionará como filtro.", target="fuel_avg"),
                    src.app_plots.AllTimeAvg("fuel_avg").register_callback(app)
                ], color="secondary", outline=True)
            ], md=6
            ),
            dbc.Col(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Card([
                                dbc.CardBody(
                                    children = [
                                        dbc.Container(
                                        dcc.Markdown("Valores de venda - máximos e mínimos", className="text-center mt-2")
                                        )                           ,
                                        dbc.Container(id = "city_summary_table"),
                                        src.app_plots.CityOverview("city_summary_table").register_callback(app),
                                    ],
                                    className="p-0"
                                )
                                ],
                                color="secondary", outline=True, 
                            )
                        ]
                    ),
                ], md=6
            ),

        ], className="mb-4"
    ),




    
    dbc.Row(
        children=[
            dbc.Col([
                dbc.Card([
                    dbc.Container(
                        dcc.Loading(
                            id="bar-plot-loader",
                            type="default",
                            children=[
                                dbc.Container(
                                    dcc.Graph(id="cities-avg-price"),
                                    id="cities-avg-price-graph-container",
                                )
                            ]
                        ),
                    ),
                    dbc.Tooltip("Clique e arraste no gráfico para selecionar uma faixa de tempo que também funcionará como filtro.", target="fuel_avg"),
                    src.app_plots.CitiesTimeAvg("cities-avg-price").register_callback(app)
                ], color="secondary", outline=True)
            ], md=12
            ),
        ]
     )

    ], style={"position":"relative", "top":"40px", "padding": "30px"}
     , fluid=True
)
            
if __name__ == "__main__":
  app.run(debug=True, 
            port=8090
         )
