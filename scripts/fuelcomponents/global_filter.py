from dash import dcc, callback, Output, Input

@callback(
    Output('global-filter-store2', 'data'),
    Input('city_dropdown', 'value'),
    Input('year_slider_class', 'value'),
    # Input('city_sel', 'value'),
    # Input('main_slider', 'value'),
)
def update_filter_store(city, year):
    return {"Municipio": city, "Ano": year}