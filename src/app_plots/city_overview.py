from dash import callback, Output, Input, dash_table, no_update
import pandas as pd

class CityOverview():
    
    def __init__(self, component_id):
        self.component_id = component_id
        
    def register_callback(self, app):
        @app.callback(
            Output("city_summary_table", "children"),
            Input('filtered-selection', 'data'),
            Input("filtered-dataset", "data")
        )
        def update_datatable(filter_selections, filtered_data):
            """
            Callback function to generate and return a Dash DataTable.
            The table is updated according to a slider that must be used to specify the year range.
            """
            if filter_selections["Municipio"] == []:
                print(f"Table won't be updated! No 'Municipio' was selected.")
                return no_update
            if filter_selections["Produto"] == []:
                print(f"Table won't be updated! No 'Produto' was selected.")
                return no_update
            else:
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

                df = pd.DataFrame.from_dict(filtered_data)
                city_overall = df
                city_overall = city_overall.groupby(["Municipio","Ano","Produto"]).agg({"Revenda":"nunique", "Valor de Venda":["min","max"]}).reset_index()

                new_column_names = []

                # Fixes the multilevel column generated when "Valor de Venda" was aggregated by "min" and "max" at the same time.
                for cols in city_overall.columns:
                    # This only works for the top and adjacent level right below it.
                    new_col_name = f'{cols[0]}_{cols[1]}'
                    new_column_names.append(new_col_name)
                city_overall.columns = new_column_names
                city_overall.columns = ['Municipio', 'Ano', 'Produto', 'Numero de Revendas', 'Valor de Venda (min)', 'Valor de Venda (max)']

                table = dash_table.DataTable(
                    id="city_summary",
                    columns=[{"name": i, "id": i} for i in city_overall.columns],
                    data = city_overall.to_dict('records'),
                    sort_action="native",
                    filter_action="native",
                    page_size=30,
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Municipio', 'Produto']
                    ],
                    **presentation_props,
                )
                return table