from dash import callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dfgen

data = dfgen.all_time_avg()
# .sort_values("Municipio",ascending=True),

@callback(Output("city_alltime_avg", "figure"),
          Input("city_sel", "value")
         )

def update_avg_barchart(city_selection):
    if city_selection == []:
        chart_data = data.sort_values("Municipio",ascending=True)
    else:
        chart_data = data[data["Municipio"].isin(city_selection)].sort_values("Municipio",ascending=True)
    figure = px.bar(
        data_frame = chart_data,
        title = "Média normalizada por cidade",
        x = "Municipio",
        y = "Normalized",
        color = "Produto",
    )
    figure.update_layout(
        margin = go.layout.Margin(t=50, b=30)
    )
    return figure