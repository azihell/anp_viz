from dash import callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# daily_fuel_avg = dfgen.daily_average_price()

@callback(Output("fuel_avg", "figure"),
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