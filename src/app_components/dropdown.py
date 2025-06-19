from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd

class MyDropdown:
    def __init__(self, component_id, option_list, initial_values=None, placeholder=None):
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
    
    def render(self):
        """
        Returns:
            dcc.Dropdown: A Dash dropdown list. Must be called from within a container.
        """
        return dcc.Dropdown(
                # dbc.Container([
                    id=self.component_id,
                    options=self.options,
                    value=self.value,
                    multi=True
                )
            # html.Div(id=self.output_container_id) # The output container for this specific dropdown
            # ]),
    # @callback(
    #     Output("product_dropdown", "options"),
    #     Input("product_dropdown", "value"),
    #     State("filtered-dataset", "data")
    # )
    # def abc(ghi, abc):
    #     df = pd.DataFrame.from_dict(ghi)
    #     print(df.head(5))
    #     sel_prods = df.loc[:, "Produto"].unique().tolist()
    #     return sel_prods
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