from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import datetime as dt
from app_data.dfgen import data_load

class Crossfilter():
    def __init__(self):

        """
        Recalculates the dataset and possible selections according to all filters selected by listening to all selection callbacks
        """
        pass

    @callback(
        # Output('filtered-selection', 'data'),
        Output('filtered-dataset', 'data'),
        Input('city_dropdown', 'value'),
        Input('year_slider_class', 'value'),
        Input("product_dropdown", "value"),
        State('filtered-selection', 'data')
    )
    def current_filter_selection(city, year, product, previous_selection):
        """
        Watches all available inputs and saves the selections in memory.
        """
        # changed_key = None
        current_selection = {"Municipio": city, "Ano": year, "Produto": product}
        # Internally patches previous state in case it initializes with "Null"
        if all(value is None for value in previous_selection.values()):
            previous_selection = current_selection
            print("ALERT: previous filter state was 'None', so it was fixed")
        
        ano_check = data_load().loc[:, "Ano"].isin(current_selection["Ano"])
        municipio_check = data_load().loc[:, "Municipio"].isin(current_selection["Municipio"])
        produto_check = data_load().loc[:, "Produto"].isin(current_selection["Produto"])

        if current_selection["Municipio"] == [] or current_selection["Produto"] == []: 
            plot_data = data_load()[ano_check]
        else:
            plot_data = data_load()[municipio_check & ano_check & produto_check]
        return plot_data.to_dict(orient='records')

        # This must be kept for normality (but bad behavior).
        selected_municipio_list = city or data_load().loc[:, "Municipio"].unique().tolist()
        selected_year_list = year or data_load().loc[:, "Ano"].unique().tolist()
        selected_product_list = product or data_load().loc[:, "Produto"].unique().tolist()
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
    
    @callback(
        Output("product_dropdown", "options"),
        Input("filtered-dataset", "data")
    )
    def abc(abc):
        df = pd.DataFrame.from_dict(abc)
        sel_prods = df.loc[:, "Produto"].unique().tolist()
        return sel_prods
