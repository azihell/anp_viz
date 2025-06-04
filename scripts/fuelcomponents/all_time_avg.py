from dash import callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dfgen

daily_fuel_avg = dfgen.daily_average_price()

@callback(Output("fuel_avg", "figure"),
          Input("main_slider", "value")
         )
def update_all_time(slider_value):
    figure = px.line(
        daily_fuel_avg.reset_index()[daily_fuel_avg.Ano.between(slider_value[0], slider_value[1])],
        title = "Média diária de preços em todos os postos",
        x = "Data da Coleta",
        y = "Valor de Venda medio",
        color = "Produto",
        
    )
    figure.update_layout(
        margin = go.layout.Margin(t=50, b=30)
    )
    return figure