from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import sys
# 
sys.path.append("./scripts")
sys.path.append("./scripts/fuelcomponents")
sys.path.append("./scripts/fuelproject_tables")
from fuelproject_tables import dfgen
from fuelcomponents import year_slider, all_time_avg

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dcc.Markdown("## ANP retail data "),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4("Select a range in years"),
            year_slider.chart(),
            dcc.Graph(
                id = "fuel_avg",
            ),
        ]),
    ]),
    #     dbc.Col([
    #         html.H4("Select a range in years"),
    #         dcc.RangeSlider(
    #             id = "slider",
    #             min = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
    #             max = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
    #             value = [
    #                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-5],
    #                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
    #                     ],
    #             step = 1,
    #             marks = {i: str(i) for i in range(
    #                         daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
    #                         daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
    #                         1)
    #                     },
    #         ),
    #         dash_table.DataTable(
    #             id = "tbl_out",
    #             data = city_overall.to_dict('records'),
    #             columns=[{"name": i, "id": i} for i in city_overall.columns],
    #             sort_action="native",
    #             page_size=10,
    #             merge_duplicate_headers=True
    #         )
    #     ])
    # ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = "city_alltime_avg",
                figure = px.bar(
                    dfgen.all_time_avg().sort_values("Municipio",ascending=True),
                    title = "City all-time average, all products",
                    x = "Municipio",
                    y = "Normalized",
                    color = "Produto",
                )
            ),
        ])
    ])
])

if __name__ == "__main__":
  app.run(jupyter_mode="external")