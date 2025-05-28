from dash import dcc
import sys
import dfgen


def year_slider():
    return print("Ran year_slider.py")
#     daily_fuel_avg = dfgen.daily_average_price()
#     dcc.RangeSlider(
#         id = "component_id",
#         min = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
#         max = daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
#         value = [
#                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-5],
#                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1]
#                 ],
#         step = 1,
#         marks = {i: str(i) for i in range(
#                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[0],
#                     daily_fuel_avg["Data da Coleta"].dt.year.unique().tolist()[-1],
#                     1)
#                 },
#     ),