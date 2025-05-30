from dash import callback, Output, Input, dash_table
import pandas as pd
import dfgen

city_overall = dfgen.city_overall()

@callback(
    Output("city_summary_over_year", "children"),
    [Input("main_slider", "value")]
)
def update_datatable(slider_value):
    """
    Callback function to generate and return a Dash DataTable.
    The table is generated only when the 'Load Data' button is clicked.
    """

    presentation_props = {
        "fixed_rows": {"headers": True},
        "style_table": {"overflowX":"auto",
                        "overflowY":"auto",
                        "height": 400},
        "style_cell": {"textAlign": "left", 
                       "padding": "5px"},
        "style_header": {"backgroundColor": "rgb(230, 230, 230)",
                         "fontSize": "12px",
                         "fontFamily": "Helvetica",
                         "fontWeight": "bold",
                         "whiteSpace": "normal"},
        "style_data": {"fontSize": "12px",
                       "fontFamily": "Helvetica"},
    }

    if not slider_value:
        return dash.no_update
    table = dash_table.DataTable(
        id="city_summary",
        columns=[{"name": i, "id": i} for i in city_overall.columns],
        data = city_overall[city_overall.Ano.between(slider_value[0], slider_value[1])].to_dict('records'),
        sort_action="native",
        page_size=20,
        **presentation_props
    )
    return table
    # return html.P("Click 'Load Data' to display the table.")