from dash import Dash, dcc #, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import sys
# 
sys.path.append("./scripts")
sys.path.append("./scripts/app_components")
sys.path.append("./scripts/fuelcomponents")
sys.path.append("./scripts/fuelproject_tables")
import app_components.crossfilter
# import app_data.dfgen
# from fuelproject_tables import dfgen
from fuelcomponents import year_slider, offcanvas
#, all_time_avg, global_filter, navbar, city_avg, city_overview
import app_components, app_data
from app_plots import all_time_avg

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
load_figure_template("SLATE")
theme = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[theme, dbc_css, dbc.icons.FONT_AWESOME])

# Top navigation bar object creation:
navbar_class = app_components.MyNavbar("top_bar", None)
navbar_class.register_callbacks(app)

app.layout = dbc.Container(children=[
    dcc.Store(id='filtered-selection',
        data={"Municipio":None, "Ano":None, "Produto":None}
        ),
    dcc.Store(id="all-possible",
              data={"Municipio":None, "Ano":None, "Produto":None}
              ),
    dcc.Store(id="filtered-dataset",
              data={}
              ),
    # Top navigation bar render method
    navbar_class.render(),
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
            # dbc.Col([
            #     dbc.Card(children=[dcc.Graph(id = "city_alltime_avg")],
            #              color="secondary", outline=True
            #         )
            # ], width = 3),
            dbc.Col([
                dbc.Card([
                    dbc.Container(id = "city_summary_table")    # html.Div(id="city_summary_over_year") works too
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
  app.run(debug=True, port=8060)