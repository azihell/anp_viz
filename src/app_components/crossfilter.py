import pandas as pd
import plotly.io as pio
from datetime import datetime
from dash import callback, Input, Output, State, no_update, ctx, Patch, clientside_callback
from dash_extensions.enrich import Serverside
from src.app_data.dfgen import data_load
from dash.exceptions import PreventUpdate

class Crossfilter:
    def __init__(self):

        """
        Recalculates the dataset and possible selections according to all filters selected by listening to all selection callbacks
        """
        DataLoad = data_load()
        self.all_municipio_list = DataLoad.loc[:, "Municipio"].unique().tolist()
        self.all_ano_list = DataLoad.loc[:, "Ano"].unique().tolist()
        self.all_produto_list = DataLoad.loc[:, "Produto"].unique().tolist()

    def register_callback(self, app):

        ####################
        # Startup callback #
        ####################

        @app.callback(
            Output('all-possible-values', 'data'),
            Output('city_dropdown', 'value', allow_duplicate=True),
            Output('year_slider_class', 'value'),
            Output('product_dropdown', 'value', allow_duplicate=True),
            Input('store-first-load-flag', 'data'),
        )
        def initial_setup(flag):
            if flag is None:
                print("-"*80)
                print(f"Program starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("Setting filter options:")
                print(f"Distinct values loaded: \n"
                      f"\t{len(self.all_municipio_list)} cities \n"
                      f"\t{len(self.all_ano_list)} years \n"
                      f"\t{len(self.all_produto_list)} products"
                )
                return {"Municipio": self.all_municipio_list, "Ano": self.all_ano_list, "Produto": self.all_produto_list}, \
                       sorted(self.all_municipio_list), [self.all_ano_list[0], self.all_ano_list[-1]], sorted(self.all_produto_list)

        #################
        # Main callback #
        #################

        @app.callback(
            Output('filtered-dataset', 'data'),
            Output('filtered-selection', 'data'),
            Input('city_dropdown', 'value'),
            Input('year_slider_class', 'value'),
            Input("product_dropdown", "value"),
            Input('fuel_avg', 'relayoutData'),
            prevent_initial_call=True
        )
        def current_filter_selection(city,
                                     year,
                                     product,
                                     line_plot_data,
                                ):
            current_selection = {"Municipio": city, "Ano": year, "Produto": product}

            # if ctx.triggered_id == "city_dropdown":
            #     print("Main callback: City trigger")
            # if ctx.triggered_id == "year_slider_class":
            #     print("Main callback: Year trigger")
            # if ctx.triggered_id == "product_dropdown":
            #     print("Main callback: Product trigger")
            # if ctx.triggered_id == 'all-possible-values':
            #     print("Main callback first time rolling.")
            # if ctx.triggered_id == "fuel_avg":
            #     print("Plot trigger")

            DataLoad = data_load()
            ano_check = DataLoad.loc[:, "Ano"].isin(list(range(current_selection["Ano"][0], current_selection["Ano"][1]+1)))
            municipio_check = DataLoad.loc[:, "Municipio"].isin(current_selection["Municipio"])
            produto_check = DataLoad.loc[:, "Produto"].isin(current_selection["Produto"])
            if line_plot_data is not None:
                if "xaxis.range[0]" in line_plot_data:
                    start_date = line_plot_data["xaxis.range[0]"]
                    end_date = line_plot_data["xaxis.range[1]"]
                    start_date_check = DataLoad.loc[:, "Data da Coleta"] >= start_date
                    end_date_check = DataLoad.loc[:, "Data da Coleta"] <= end_date
                    return Serverside(DataLoad[ano_check & municipio_check & produto_check & start_date_check & end_date_check]), current_selection
            return Serverside(DataLoad[ano_check & municipio_check & produto_check]), current_selection
 
        # All cities button behavior
        @app.callback(
            Output('city_dropdown', 'value', allow_duplicate=True),
            Input('select-all-cities-button', 'n_clicks'),
            State('city_dropdown', 'options'),
            prevent_inital_call=True
        )
        def button_action(cities_button, cities_state):
            if cities_button is not None:
                return cities_state
            
        # All products button behavior
        @app.callback(
            Output('product_dropdown', 'value', allow_duplicate=True),
            Input('select-all-products-button', 'n_clicks'),
            State('product_dropdown', 'options'),
            prevent_inital_call=True
        )
        def button_action(products_button, products_state):
            if products_button is not None:
                return products_state

        @app.callback(
            Output('city_dropdown', 'options'),
            Output('product_dropdown', 'options'),
            Input('filtered-selection', 'data'),
            State('city_dropdown', 'options'),
            State('product_dropdown', 'options')
        )
        def dropdown_choices(filter_selections, last_valid_city, last_valid_product):
            if filter_selections["Municipio"] == []:
                return last_valid_city, no_update
            if filter_selections["Produto"] == []:
                return no_update, last_valid_product
            # Full dataset with all possible combinations among columns needs to be loaded
            DataLoad = data_load()
            # Applies current filters in full dataset to discover possible cities can be selected
            product_check = DataLoad.loc[:, "Produto"].isin(filter_selections["Produto"])
            year_check = DataLoad.loc[:, "Ano"].isin(list(range(filter_selections["Ano"][0], filter_selections["Ano"][1]+1)))
            filtered_df = DataLoad[product_check & year_check]
            remaining_cities = filtered_df["Municipio"].unique().tolist()
            # Applies current filters in full dataset to discover possible products can be selected
            city_check = DataLoad.loc[:, "Municipio"].isin(filter_selections["Municipio"])
            year_check = DataLoad.loc[:, "Ano"].isin(list(range(filter_selections["Ano"][0], filter_selections["Ano"][1]+1)))
            filtered_df = DataLoad[city_check & year_check]
            remaining_products = filtered_df["Produto"].unique().tolist()
            # Returns possible selections 
            return sorted(remaining_cities), sorted(remaining_products)

        @app.callback(
            Output('bad-filtering-popup', 'is_open'),
            Input('filtered-selection', 'data')
        )
        def bad_filtering(filter_selections):
            if filter_selections["Municipio"] == [] or filter_selections["Produto"] == []:
                return True
            else:
                return False