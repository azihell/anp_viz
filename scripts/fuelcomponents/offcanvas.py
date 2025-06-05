import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from fuelcomponents import year_slider, city_dropdown
from fuelproject_tables import dfgen

city_list = dfgen.city_overall()["Municipio"].unique()

def generate_offcanvas():
    offcanvas = html.Div(
        [
            dbc.Offcanvas(
                children=[
                    dbc.Container([
                        dbc.Card([
                            dbc.CardHeader("Anos"),
                            dbc.CardBody([
                                    year_slider.chart("main_slider")
                                ])
                            ], color="secondary", outline=True
                        ),
                        dbc.Card([
                            dbc.CardHeader("Cidades"),
                            dbc.CardBody([
                                city_dropdown.chart("city_sel")
                                ])
                            ], color="secondary", outline=True
                        ),
                    ], # className="d-flex flex-column gap-3", style={"height": "100%", "padding": "15px"}
                    )
                ],
                id="offcanvas-scrollable",
                scrollable=True,
                title="Filtros",
                is_open=False,
                keyboard=True,
                close_button=False,
                class_name="g-2"
            ),
        ]
    )
    return offcanvas