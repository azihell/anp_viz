from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from fuelproject_tables import dfgen

daily_fuel_avg = dfgen.daily_average_price()
minYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0]
maxYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]

def chart(referred_chart):
    """
    Generates the chart for this script. It is a slide bar to select the years of data available. These years are obtained from the main dataset or a trusty derivative.
    
    Parameters:
    referred_chart (str): id of the chart this slide bar will act on.

    Returns:
      year_slider
    A RangeSlider object from the Dash package.
    """
    year_slider = dbc.Container([
        dcc.RangeSlider(
            id = referred_chart,
            min = minYear,
            max = maxYear,
            value = [daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                        daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
                    ],
            step = 1,
            marks={
                minYear: {'label': minYear, 'style': {'color': '#77b0b1'}},    # Label for the minimum value
                maxYear: {'label': maxYear, 'style': {'color': '#f50'}} # Label for the maximum value
            },
            tooltip={"placement": "top",
                        "style": {"color": "White", "fontSize": "12px"},
            },
            dots=True
        ),
    ])
    return year_slider