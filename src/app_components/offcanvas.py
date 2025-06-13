import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from .dropdown import MyDropdown
from .slider import MyRangeSlider
from fuelproject_tables import dfgen
# from fuelcomponents import year_slider, city_dropdown

# City list dropdown component object creation
cities_list = dfgen.city_overall()["Municipio"].unique().tolist()
city_dropdown = MyDropdown("city_dropdown", cities_list)
# city_dropdown.register_callbacks(app)

# Years range slider creation
daily_fuel_avg = dfgen.daily_average_price()
marks_list = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()
marks = {value: str(value) for value in marks_list}
minYear = marks_list[0]
maxYear = marks_list[-1]
default_values = [minYear, maxYear]
year_slider = MyRangeSlider("slider_class", minYear, maxYear, marks, default_values)

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
            offcanvas: A side menu containing filters for custom data navigation
        """
        offcanvas = html.Div(
            [
                dbc.Offcanvas(
                    children=[
                        dbc.Container([
                            dbc.Card([
                                dbc.CardHeader("Anos"),
                                dbc.CardBody([
                                    year_slider.render()
                                        # year_slider.chart("main_slider")
                                    ])
                                ], color="secondary", outline=True
                            ),
                            dbc.Card([
                                dbc.CardHeader("Cidades"),
                                dbc.CardBody([
                                    city_dropdown.render()
                                    # city_dropdown.chart("city_sel")
                                    ])
                                ], color="secondary", outline=True
                            ),
                        ],
                        )
                    ],
                    id=self.component_id,
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