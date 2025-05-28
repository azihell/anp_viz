from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dfgen

daily_fuel_avg = dfgen.daily_average_price()

def chart():
    """
    Generates the chart for this script. It is a slide bar to select the years of data available
    """

    rangebar = dbc.Container([
        html.A(
            dcc.RangeSlider(
                id = "all_time_slider",
                min = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
                max = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                value = [
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-5],
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
                        ],
                step = 1,
                marks = {i: str(i) for i in range(
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                            1)
                        },
            ),
        )
    ])
    return rangebar