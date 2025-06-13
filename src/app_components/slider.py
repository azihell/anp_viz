from dash.dcc import RangeSlider #, html, callback, Output, Input, State
from dash_bootstrap_components import Container

# daily_fuel_avg = dfgen.daily_average_price()
# minYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0]
# maxYear = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
class MyRangeSlider:
    def __init__(self, component_id, min, max, marks, starting_values):
        """
        Generates a slide bar to select from a range of data.
        The range shall be defined outside this object.
        
        Args:
            component_id (str): unique ID for this chart. Can be used by a different component to read from it
            min (str): minimum value on the range
            max (str): maximum value on the range
            marks (str): when defined, limits the values selectable on the bar. Otherwise, the possible values will range from min to max with 1 as a step

        Returns:
            A RangeSlider object from the Dash package.
        """
        self.component_id = component_id
        self.min = min
        self.max = max
        self.marks = marks        
        self.starting_values = starting_values        
        
    def render(self):
        """
        Returns:
            dcc.Rangeslider: A Dash core component RangeSlider. Must be called from within a container.
        """
        range_slider = RangeSlider(
                id = self.component_id,
                min = self.min,
                max = self.max,
                step = None if self.marks is not None else 1,
                marks = self.marks,
                value = self.starting_values,
                tooltip={"placement": "top",
                            "style": {"color": "White", "fontSize": "12px"},
                },
                dots=True
            )
        return range_slider