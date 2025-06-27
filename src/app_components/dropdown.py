from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd

class MyDropdown:
    def __init__(self, component_id, option_list, placeholder, dimension, initial_values=None):
        """
        Initializes a Dropdown component.

        Args:
            component_id (str): The ID for the dcc.Dropdown component. This is crucial for callbacks.
            output_container_id (str): The ID of the html.Div component where the output of this dropdown's callback will be displayed.
            initial_values (list, optional): A list of city names to pre-select. Defaults to ["Feira De Santana", "Salvador"].
        """
        self.component_id = component_id
        self.options = option_list
        self.value = initial_values
        self.placeholder = placeholder
        self.dimension = dimension
    def render(self):
        """
        Returns:
            dcc.Dropdown: A Dash dropdown list. Must be called from within a container.
        """
        return dcc.Dropdown(
                    id=self.component_id,
                    options=self.options,
                    value=self.value,
                    multi=True,
                    placeholder=self.placeholder,
                    maxHeight=300
                )
    def register_callback(self):
        @callback(
            Output(self.component_id, "options"),
            Input("filtered-selection", "data"),
            Input("all-possible-values", "data"),
            Input("remaining-choices", "data")
        )
        def cbk_function(filtered_selection, all_possible, remains):
            unselected_cities = (list(set(all_possible[self.dimension])-set(filtered_selection[self.dimension])))
            style_present_values = {'color': 'Black', 'font-size': 12}
            style_absent_values = {'color': 'Red', 'font-size': 12}
            dropdown_options = []
            for item in filtered_selection[self.dimension]:
                dropdown_options.append({
                    "label": html.Span([item], style=style_present_values),
                    "value": item,
                })
            for item in (list(set(all_possible[self.dimension])-set(filtered_selection[self.dimension]))):
                dropdown_options.append({
                    "label": html.Span([item], style=style_absent_values),
                    "value": item,
                })
            return dropdown_options