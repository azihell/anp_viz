from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc

class MyDropdown:
    def __init__(self, component_id, option_list, initial_values=None):
        """
        Initializes a Dropdown component.

        Args:
            component_id (str): The ID for the dcc.Dropdown component. This is crucial for callbacks.
            output_container_id (str): The ID of the html.Div component where the output of this dropdown's callback will be displayed.
            initial_values (list, optional): A list of city names to pre-select. Defaults to ["Feira De Santana", "Salvador"].
        """
        self.component_id = component_id
        # self.output_container_id = output_container_id
        self.options = option_list
        self.value = initial_values if initial_values is not None else ["Feira De Santana", "Salvador"]
    
    def render(self):
        """
        Renders the dcc.Dropdown component within a dbc.Container
        and its associated output container.

        Returns:
            html.Div: A Dash HTML Div containing the dropdown and its output.
        """
        return dbc.Container([
                dcc.Dropdown(
                    id=self.component_id,
                    # options=[{'label': city, 'value': city} for city in self.options],
                    options = self.options,
                    value=self.value,
                    multi=True
                ),
            # html.Div(id=self.output_container_id) # The output container for this specific dropdown
            ]),

    # def register_callbacks(self, app):
    #     """
    #     Stores the selection for filtering.

    #     Args:
    #         app (dash.Dash): The Dash application instance.
    #     """
    #     @app.callback(
    #         Output(self.output_container_id, "children"),
    #         Input(self.component_id, "value")
    #     )
    #     def update_output(selected_cities):
    #         if selected_cities:
    #             print(f"Callback triggered! Input value: {selected_cities}") # This will print to the terminal
    #             return f"Selected Cities for {self.component_id}: {', '.join(selected_cities)}"
    #         return f"No cities selected for {self.component_id}"