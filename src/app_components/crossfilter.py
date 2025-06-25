from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from app_data.dfgen import data_load

class Crossfilter:
    def __init__(self):

        """
        Recalculates the dataset and possible selections according to all filters selected by listening to all selection callbacks
        """
        self.all_municipio_list = data_load().loc[:, "Municipio"].unique().tolist()
        self.all_ano_list = data_load().loc[:, "Ano"].unique().tolist()
        self.all_produto_list = data_load().loc[:, "Produto"].unique().tolist()

    def register_callback(self, app):

        #################
        # Main callback #
        #################

        @app.callback(
            Output('filtered-dataset', 'data'),
            Output('filtered-selection', 'data'),
            Output('all-possible', 'data'),
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
            
            ano_check = data_load().loc[:, "Ano"].isin(current_selection["Ano"])
            municipio_check = data_load().loc[:, "Municipio"].isin(current_selection["Municipio"])
            produto_check = data_load().loc[:, "Produto"].isin(current_selection["Produto"])
            if current_selection["Municipio"] == [] or current_selection["Produto"] == []: 
                plot_data = data_load()[ano_check]
            else:
                plot_data = data_load()[municipio_check & ano_check & produto_check]

            return plot_data.to_dict(orient='records'), current_selection, full_dataset
        
        # Load values of the city dropdown component. They are based on the full city dataset seen on the __init__ function.
        @app.callback(
            Output('city_dropdown', 'value'),
            Output('product_dropdown', 'value'),
            Input('url', 'pathname'),
            Input('year_slider_class', 'value'),
            State('city_dropdown', 'value')
        )

        def starting_vals(url, other, city_list):
            if not city_list:
                print("State is Null!!")
                return self.all_municipio_list, self.all_produto_list

        @app.callback(Output("fuel_avg", "figure"),
                Input("filtered-dataset", "data"),
                )
        def update_all_time(filter_data):
            # Data preparation
            df = pd.DataFrame.from_dict(filter_data)
            daily_fuel_avg = df.groupby(["Produto","Data da Coleta","Ano","Municipio"])["Valor de Venda"].agg(["mean"]).reset_index()
            daily_fuel_avg.columns = ["Produto", "Data da Coleta", "Ano", "Municipio", "Valor de Venda medio"]
            # Figure rendering
            figure = px.line(
                daily_fuel_avg,
                title = "Média diária de preços em todos os postos",
                x = "Data da Coleta",
                y = "Valor de Venda medio",
                color = "Produto",
                
            )
            figure.update_layout(
                margin = go.layout.Margin(t=50, b=30)
            )
            return figure



            # This must be kept for normality (but bad behavior).
            # return {"Municipio": selected_municipio_list, "Ano": selected_year_list, "Produto":selected_product_list}, {"Test": "Nothing"}
            # return {"Municipio": selected_municipio_list, "Ano": selected_year_list, "Produto":selected_product_list}

        # @callback(
        #     Output("filtered-dataset", "data"),
        #     Input("filtered-selection", "data"),
        # )
        # def main_data_updater(filter_data):
        #     ano_list = filter_data.get("Ano")
        #     municipio_list = filter_data.get("Municipio")
        #     produto_list = filter_data.get("Produto")
        #     ano_check = data_load().loc[:, "Ano"].isin(ano_list)
        #     municipio_check = data_load().loc[:, "Municipio"].isin(municipio_list)
        #     produto_check = data_load().loc[:, "Produto"].isin(produto_list)
        #     if municipio_list == [] or produto_list == []: 
        #         plot_data = data_load()[ano_check]
        #     else:
        #         plot_data = data_load()[municipio_check & ano_check & produto_check]
        #     return plot_data.to_dict(orient='records')
        
        # @callback(
        #     Output("product_dropdown", "options"),
        #     Input("filtered-dataset", "data")
        # )
        # def abc(abc):
        #     df = pd.DataFrame.from_dict(abc)
        #     sel_prods = df.loc[:, "Produto"].unique().tolist()
        #     return sel_prods
