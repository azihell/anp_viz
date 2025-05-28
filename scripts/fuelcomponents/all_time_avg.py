from dash import callback, Output, Input
import plotly.express as px
import dfgen

daily_fuel_avg = dfgen.daily_average_price()

@callback(Output("fuel_avg", "figure"),
          Input("all_time_slider", "value")
         )
def update_all_time(slider_value):
    figure = px.line(
        daily_fuel_avg.reset_index()[daily_fuel_avg.Ano.between(slider_value[0], slider_value[1])],
        title = "Daily avg by fuel - all gas stations",
        x = "Data da Coleta",
        y = "Valor de Venda medio",
        color = "Produto"
    )
    return figure