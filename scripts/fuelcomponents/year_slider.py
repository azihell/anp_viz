from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dfgen

daily_fuel_avg = dfgen.daily_average_price()

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
        html.A(
            dcc.RangeSlider(
                id = referred_chart,
                min = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
                max = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                value = [daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                        daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
                        ],
                step = 1,
                marks = {i: str(i) for i in range(
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
                            daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
                            1)
                        },
                tooltip={"placement": "top",
                        # "always_visible": True,
                        "style": {"color": "White", "fontSize": "12px"
                        },
    },
            ),
        )
    ])
    return year_slider