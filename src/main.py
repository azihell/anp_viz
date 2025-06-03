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
from fuelcomponents import year_slider, all_time_avg, city_overview, sidebar

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
load_figure_template("SLATE")
theme = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[theme, dbc_css])

SIDEBAR_WIDTH = "250px"

OFFCANVAS_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": SIDEBAR_WIDTH,
    "padding": "1rem", # Add some padding inside the sidebar
    "background-color": "#f8f9fa", # Light gray background for the sidebar
    "box-shadow": "2px 0 5px rgba(0,0,0,0.1)", # Subtle shadow
    "z-index": 1040, # Ensure it's above other content but below modals
    "overflow": "visible", # Enable vertical scrolling if content overflows
}


app.layout = dbc.Container([
    dbc.Offcanvas(
            dcc.Markdown("XYZ"),
            id="always-open-sidebar",
            is_open=True,          # Make it always open
            backdrop=False,        # Prevent closing when clicking outside
            close_button=False,    # Remove the close button
            scrollable=True,       # Allow content to scroll if it's too long
            placement="start",     # Position it on the left (can be "end" for right)
            # style=OFFCANVAS_STYLE, # Apply the custom fixed sidebar style
            style={"width": SIDEBAR_WIDTH, 'padding': '10px', "background-color": "rgb(50, 56, 62)"}
    ),
    dbc.Container(
    style={'width': '100%', 'padding': '10px', "position":"relative", "left":SIDEBAR_WIDTH},
    # className="dbc",    # Uncomment to enable DataTable to be styled according to the theme selected. But loses "style_as_list_view" : True," property while at it.
    children = [
        dbc.Row([
        dcc.Markdown("### Histórico de preços de combustível"),
        dcc.Markdown("Baseado em *dataset* da Agência Nacional de Petróleo e Gás. [Disponível no Kaggle](https://www.kaggle.com/datasets/paulogladson/anp-combustveis) e generosamente compilado por [Paulo Gladson](https://github.com/PauloGladson)."),
        html.Br(),
        dbc.Col(
            children = [
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader("Escolha uma faixa (em anos) como filtro:"),
                        dbc.CardBody([
                                year_slider.chart("main_slider")
                            ])
                    ], color = "secondary", outline = True
                    ),
                    dbc.Col([
                    
                    dbc.Card([
                        dcc.Graph(id = "fuel_avg", style={"max-height":"100%"}),
                    ], color = "secondary", outline = True)

                    ], style={"max-width":"100%", "position":"relative"}),
                    dbc.Col([
                    
                    dbc.Card([
                        dbc.Container(id = "city_summary_over_year")    # html.Div(id="city_summary_over_year") works too
                    ], color="secondary", outline=True)

                    ], style={"max-width":"100%", "position":"relative"}),

                ])
            ]
        ),

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
    ])
])

if __name__ == "__main__":
  app.run()