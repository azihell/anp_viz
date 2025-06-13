from dash.dcc import RangeSlider #, html, callback, Output, Input, State
from dash_bootstrap_components import Container

# daily_fuel_avg = dfgen.daily_average_price()
# minYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0]
# maxYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
class MyRangeSlider:
    def __init__(self, component_id, min, max, marks, starting_values):
        """
        Generates the chart for this script. It is a slide bar to select the years of data available. These years are obtained from the main dataset or a trusty derivative.
        
        Parameters:
        referred_chart (str): id of the chart this slide bar will act on.

        Returns:
        year_slider
        A RangeSlider object from the Dash package.
        """
        self.component_id = component_id
        self.min = min
        self.max = max
        self.marks = marks        
        self.starting_values = starting_values        
        
    def render(self):
        range_slider = Container([
            RangeSlider(
                id = self.component_id,
                min = self.min,
                max = self.max,
                step = None,
                marks = self.marks,
                value = self.starting_values,
                tooltip={"placement": "top",
                            "style": {"color": "White", "fontSize": "12px"},
                },
                dots=True
            ),
        ])
        return range_slider