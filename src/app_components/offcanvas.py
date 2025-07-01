import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from .dropdown import MyDropdown
from .slider import MyRangeSlider
from app_data.dfgen import data_load

# City list dropdown component object creation
cities_list = data_load()["Municipio"].unique().tolist()
city_dropdown = MyDropdown(
    component_id="city_dropdown",
    option_list=cities_list,
    placeholder="Escolha uma cidade:",
    dimension="Municipio"
    )
# Products dropdown
products_list = data_load()["Produto"].unique().tolist()
product_dropdown = MyDropdown(
    component_id="product_dropdown",
    option_list=products_list,
    placeholder="Escolha um produto",
    dimension="Produto"
    )

# Years range slider creation
marks_list = data_load()["Data da Coleta"].dt.year.unique().tolist()
marks = {value: str(value) for value in marks_list}
minYear = marks_list[0]
maxYear = marks_list[-1]
default_values = [minYear, maxYear]
year_slider = MyRangeSlider("year_slider_class", minYear, maxYear, marks, default_values)


class MyOffcanvas:
    def __init__(self, component_id):
        """
        Initializes an Offcanvas component.
        """
        self.component_id = component_id
    def render(self):
        """
        Renders a dbc.Offcanvas component within a dbc.Container

        Returns:
            dbc.offcanvas: A Dash Bootstrap component Offcanvas. Must be called from within a container.
        """
        offcanvas = html.Div(
            [
                dbc.Offcanvas(
                    children=[
                        dbc.Container([
                            dbc.Row(
                                dbc.Card([
                                    dbc.CardHeader("Anos"),
                                    dbc.CardBody([
                                        year_slider.render()
                                        ])
                                    ], color="secondary", outline=True
                                ), className="mb-2"
                            ),
                            dbc.Row(
                                dbc.Card([
                                    dbc.CardHeader("Cidades"),
                                    dbc.CardBody([
                                        city_dropdown.render(),
                                        ])
                                    ], color="secondary", outline=True
                                ), className="mb-2"
                            ),
                            dbc.Row(
                                dbc.Card([
                                    dbc.CardHeader("Produtos"),
                                    dbc.CardBody([
                                        product_dropdown.render(),
                                        ])
                                    ], color="secondary", outline=True
                                ),
                            ),
                         ]),
                    ],
                    id=self.component_id,
                    scrollable=True,
                    title="Filtros",
                    is_open=False,
                    keyboard=True,
                    close_button=False,
                ),
            ]
        )
        return offcanvas