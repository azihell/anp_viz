from dash import callback, Output, Input, dash_table, no_update
import pandas as pd
import dfgen

city_overall = dfgen.city_overall()

@callback(
    Output("city_summary_over_year", "children"),
    Input("main_slider", "value")
)
def update_datatable(slider_value):
    """
    Callback function to generate and return a Dash DataTable.
    The table is updated according to a slider that must be used to specify the year range.
    """

    presentation_props = {
        "style_as_list_view" : True,
        "fixed_rows": {"headers": True},
        "style_table": {"overflowY":"auto",
                        "overflowX":"auto",
                        "height": 400},
        "style_cell": {"minWidth": "80px", "width": "auto", "maxWidth": "180px", # Responsive column widths
                       "backgroundColor": "rgb(50, 56, 62)",
                       "overflow": "hidden",
                       "textOverflow": "ellipsis",
                       "whiteSpace": "normal",
                       "padding": "5px",
                      },
        "style_filter": {"backgroundColor": "rgb(230, 230, 230)",
                         "color": "rgb(50, 56, 62)",
                         "textAlign": "center",
                        },
        "style_header": {"backgroundColor": "rgb(230, 230, 230)",
                         "color": "rgb(50, 56, 62)",
                         "textAlign": "center",
                         "fontSize": "14px",
                         "fontFamily": "Helvetica",
                         "fontWeight": "bold",
                         },
        "style_data": {"fontSize": "12px",
                       "fontFamily": "Verdana"},
    }

    if not slider_value:
        return no_update
    table = dash_table.DataTable(
        id="city_summary",
        columns=[{"name": i, "id": i} for i in city_overall.columns],
        data = city_overall[city_overall.Ano.between(slider_value[0], slider_value[1])].to_dict('records'),
        sort_action="native",
        filter_action="native",
        page_size=20,
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Municipio', 'Produto']
        ],
        **presentation_props,
    )
    return table