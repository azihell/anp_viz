from dash import callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dfgen

daily_fuel_avg = dfgen.daily_average_price()

@callback(Output("fuel_avg", "figure"),
          Input("global-filter-store", "data")
         )
def update_all_time(filter_data):
    municipio_list = filter_data.get("Municipio")
    ano_list = filter_data.get("Ano")
    municipio_check = daily_fuel_avg["Municipio"].isin(municipio_list)
    ano_check = daily_fuel_avg["Ano"].isin(ano_list)
    if municipio_list == []:
        plot_data = daily_fuel_avg
    else:
        plot_data = daily_fuel_avg[municipio_check & ano_check]
    figure = px.line(
        plot_data,
        title = "Média diária de preços em todos os postos",
        x = "Data da Coleta",
        y = "Valor de Venda medio",
        color = "Produto",
        
    )
    figure.update_layout(
        margin = go.layout.Margin(t=50, b=30)
    )
    return figure