from dash import callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dfgen

data = dfgen.all_time_avg()

@callback(Output("city_alltime_avg", "figure"),
          Input("global-filter-store", "data")
        #   Input("city_sel", "value")
         )

def update_avg_barchart(filter_data):
    municipio_list = filter_data.get("Municipio")
    ano_list = filter_data.get("Ano")
    municipio_check = data["Municipio"].isin(municipio_list)
    ano_check = data["Ano"].isin(ano_list)
    if municipio_list == []:
        # All years contribution are added
        plot_data = data.groupby(["Municipio","Produto"])["Normalized"].agg("sum").reset_index().sort_values("Municipio",ascending=True)
    else:
        plot_data = data[municipio_check & ano_check].groupby(["Municipio","Produto"])["Normalized"].agg("sum").reset_index().sort_values("Municipio",ascending=True)
    # if city_selection == []:
    #     chart_data = data.sort_values("Municipio",ascending=True)
    # else:
    #     chart_data = data[data["Municipio"].isin(city_selection)].sort_values("Municipio",ascending=True)
    figure = px.bar(
        data_frame = plot_data,
        title = "Média normalizada por cidade",
        x = "Municipio",
        y = "Normalized",
        color = "Produto",
    )
    figure.update_layout(
        margin = go.layout.Margin(t=50, b=30)
    )
    return figure