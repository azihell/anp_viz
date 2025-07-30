from dash import callback, Output, Input, no_update
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class AllTimeAvg():

    def __init__(self, component_id):
        self.component_id = component_id

    def register_callback(self, app):
        @app.callback(
            Output('fuel_avg', 'figure'),
            Output('fuel-avg-graph-container', 'style'),
            Input('filtered-dataset', 'data'),
            Input('filtered-selection', 'data'),
            )
        def update_all_time(filter_data, filter_selections):
            if filter_selections["Municipio"] == []:
                print(f"Line chart won't be updated! No 'Municipio' was selected.")
                return no_update
            if filter_selections["Produto"] == []:
                print(f"Line chart won't be updated! No 'Produto' was selected.")
                return no_update
            else:
                # Data preparation
                df = pd.DataFrame.from_dict(filter_data)
                daily_fuel_avg = df.groupby(["Produto","Data da Coleta","Ano","Municipio"])["Valor de Venda"].agg(["mean"]).reset_index()
                daily_fuel_avg.columns = ["Produto", "Data da Coleta", "Ano", "Municipio", "Valor de Venda medio"]
                # Figure rendering
                figure = px.line(
                    daily_fuel_avg,
                    title = "Média diária de preços em todos os postos",
                    x = "Data da Coleta",
                    y = "Valor de Venda medio",
                    color = "Produto",
                    
                )
                figure.update_layout(
                    margin = go.layout.Margin(t=50, b=60, l=20),
                    title={
                        'text': "Média diária de preços em todos os postos",
                        'y':0.97, # You can adjust the vertical position (0 to 1)
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                    },
                    autosize=False,
                    height=592
                )
                return figure, {'display': 'block'} 