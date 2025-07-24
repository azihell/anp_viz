from dash import dcc, callback, Input, Output, State, no_update, ctx
from dash_extensions.enrich import Serverside
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from src.app_data.dfgen import data_load
from dash.exceptions import PreventUpdate

class Crossfilter:
    def __init__(self):

        """
        Recalculates the dataset and possible selections according to all filters selected by listening to all selection callbacks
        """
        self.DataLoad = data_load()
        self.all_municipio_list = self.DataLoad.loc[:, "Municipio"].unique().tolist()
        self.all_ano_list = self.DataLoad.loc[:, "Ano"].unique().tolist()
        self.all_produto_list = self.DataLoad.loc[:, "Produto"].unique().tolist()

    def register_callback(self, app):
        # FIRST DATA LOAD
        @app.callback(
            Output('filtered-dataset', 'data'),
            Output('filtered-selection', 'data'),
            Output('city-dropdown', 'value'),
            Output('product_dropdown', 'value'),
            Input('store-first-load-flag', 'data'),
        )
        def initial_loading(flag):
            if ctx.triggered_id == "store-first-load-flag":
                print("Startup trigger ON")
            
            if(flag) is None:
                full_dataset = {"Municipio": self.all_municipio_list,
                                "Ano": self.all_ano_list,
                                "Produto": self.all_produto_list}
                print("Filling dataset and initial filter selections...")
                return Serverside(self.DataLoad), full_dataset, sorted(self.all_municipio_list), sorted(self.all_produto_list)
            
        
        @app.callback(
            Output('filtered-dataset', 'data', allow_duplicate=True),
            Output('filtered-selection', 'data', allow_duplicate=True),
            Input('city-dropdown', 'value'),
            Input('year-slider-class', 'value'),
            Input("product_dropdown", "value"),
            Input('all-possible-values', 'data'),
            # Input('fuel-avg', 'relayoutData'),
            State('filtered-selection', 'data'),
            prevent_initial_call=True,
        )
        def current_filter_selection(city,
                                     year,
                                     product, 
                                     full_dataset, 
                                    #  line_plot_data, 
                                     previous_selection):
            """
            Watches all available inputs and saves the selections in memory.
            """

            current_selection = {"Municipio": city, "Ano": year, "Produto": product}

            # if not ctx.triggered_id:
            #     print("Callback not triggered")
            # if ctx.triggered_id == "city_dropdown":
            #     print("Main callback: City trigger")
            # if ctx.triggered_id == "year_slider_class":
            #     print("Main callback: Year trigger")
            # if ctx.triggered_id == "product_dropdown":
            #     print("Main callback: Product trigger")
            # # if ctx.triggered_id == "all-possible-values":
            # #     print("Alteração nos valores")
            # if ctx.triggered_id == "fuel_avg":
            #     print("Plot trigger")

            # Internally patches previous state in case it initializes with "None"
            # if all(value is None for value in previous_selection.values()):
            #     full_dataset = {"Municipio": self.all_municipio_list, "Ano": self.all_ano_list, "Produto": self.all_produto_list}
            #     previous_selection = full_dataset
            #     print("ALERT: previous filter state was 'None', so it was fixed")
            
            DataLoad = data_load()
            ano_check = DataLoad.loc[:, "Ano"].isin(list(range(current_selection["Ano"][0], current_selection["Ano"][1]+1)))
            municipio_check = DataLoad.loc[:, "Municipio"].isin(current_selection["Municipio"])
            produto_check = DataLoad.loc[:, "Produto"].isin(current_selection["Produto"])
            # if line_plot_data is not None:
            #     if "xaxis.range[0]" in line_plot_data:
            #         start_date = line_plot_data["xaxis.range[0]"]
            #         end_date = line_plot_data["xaxis.range[1]"]
            #         start_date_check = DataLoad.loc[:, "Data da Coleta"] >= start_date
            #         end_date_check = DataLoad.loc[:, "Data da Coleta"] <= end_date
            #         return Serverside(DataLoad[ano_check & municipio_check & produto_check & start_date_check & end_date_check]), current_selection
            FiltDataLoad=DataLoad[ano_check & municipio_check & produto_check]
            print(f"{FiltDataLoad['Municipio'].unique().tolist()}")
            return Serverside(DataLoad[ano_check & municipio_check & produto_check]), current_selection