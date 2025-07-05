from dash import callback, Input, Output, State, no_update
from dash_extensions.enrich import Serverside
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from src.app_data.dfgen import data_load

class Crossfilter:
    def __init__(self):

        """
        Recalculates the dataset and possible selections according to all filters selected by listening to all selection callbacks
        """
        # self.data_load = data_load()
        DataLoad = data_load()
        self.all_municipio_list = DataLoad.loc[:, "Municipio"].unique().tolist()
        self.all_ano_list = DataLoad.loc[:, "Ano"].unique().tolist()
        self.all_produto_list = DataLoad.loc[:, "Produto"].unique().tolist()

    def register_callback(self, app):

        #################
        # Main callback #
        #################

        @app.callback(
            Output('filtered-dataset', 'data'),
            Output('filtered-selection', 'data'),
            Output('all-possible-values', 'data'),
            Input('city_dropdown', 'value'),
            Input('year_slider_class', 'value'),
            Input("product_dropdown", "value"),
            State('filtered-selection', 'data')
        )
        def current_filter_selection(city, year, product, previous_selection):
            """
            Watches all available inputs and saves the selections in memory.
            """
            full_dataset = {"Municipio": self.all_municipio_list, "Ano": self.all_ano_list, "Produto": self.all_produto_list}
            current_selection = {"Municipio": city, "Ano": year, "Produto": product}
            # Internally patches previous state in case it initializes with "Null"
            if all(value is None for value in previous_selection.values()):
                previous_selection = full_dataset
                print("ALERT: previous filter state was 'None', so it was fixed")
            
            DataLoad = data_load()

            ano_check = DataLoad.loc[:, "Ano"].isin(current_selection["Ano"])
            municipio_check = DataLoad.loc[:, "Municipio"].isin(current_selection["Municipio"])
            produto_check = DataLoad.loc[:, "Produto"].isin(current_selection["Produto"])
     
            return Serverside(DataLoad[municipio_check & ano_check & produto_check]), current_selection, full_dataset
            # return DataLoad[municipio_check & ano_check & produto_check].to_dict(orient='records'), current_selection, full_dataset


        # Load values of the city dropdown component. They are based on the full city dataset seen on the __init__ function.
        @app.callback(
            Output('city_dropdown', 'value'),
            Output('product_dropdown', 'value'),
            Input('url', 'pathname'),
        )
        def starting_vals(url):
            return self.all_municipio_list, self.all_produto_list

        @app.callback(
            Output("city_dropdown", "options"),
            Output("product_dropdown", "options"),
            Input('filtered-selection', 'data'),
            State('city_dropdown', 'options'),
            State('product_dropdown', 'options')
        )
        def dropdown_choices(filter_selections, last_valid_city, last_valid_product):
            if filter_selections["Municipio"] == []:
                return last_valid_city, no_update
            if filter_selections["Produto"] == []:
                return no_update, last_valid_product

            dataload = data_load()
            product_check = dataload.loc[:, "Produto"].isin(filter_selections["Produto"])
            year_check = dataload.loc[:, "Ano"].isin(filter_selections["Ano"])
            filtered_df = dataload[product_check & year_check]
            remaining_cities = filtered_df["Municipio"].unique().tolist()

            city_check = dataload.loc[:, "Municipio"].isin(filter_selections["Municipio"])
            year_check = dataload.loc[:, "Ano"].isin(filter_selections["Ano"])
            filtered_df = dataload[city_check & year_check]
            remaining_products = filtered_df["Produto"].unique().tolist()
            
            return remaining_cities, remaining_products

        @app.callback(
            Output('bad-filtering-popup', 'is_open'),
            Input('filtered-selection', 'data')
        )
        def bad_filtering(filter_selections):
            if filter_selections["Municipio"] == [] or filter_selections["Produto"] == []:
                return True
            else:
                return False
