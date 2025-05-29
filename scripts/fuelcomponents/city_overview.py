from dash import callback, Output, Input, dash_table
import pandas as pd
import dfgen

city_overall = dfgen.city_overall()

@callback(
    Output("city_summary_over_year", "children"),
    [Input("slider", "value")]
)
def update_datatable(slider_value):
    """
    Callback function to generate and return a Dash DataTable.
    The table is generated only when the 'Load Data' button is clicked.
    """
    if not slider_value:
        return dash.no_update
    # Create the DataTable
    table = dash_table.DataTable(
        id="city_summary_over_year",
        columns=[{"name": i, "id": i} for i in city_overall.columns],
        data =  city_overall[city_overall.Ano.between(slider_value[0], slider_value[1])].to_dict('records'),
        # style_table={'overflowX': 'auto'},
        # style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        sort_action='native',
        row_selectable='multi',
        page_size=10
    )
    return table
    # return html.P("Click 'Load Data' to display the table.")