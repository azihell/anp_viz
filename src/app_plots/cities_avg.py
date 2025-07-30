from dash import callback, Output, Input, no_update
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express.colors as px_colors

class CitiesTimeAvg():

    def __init__(self, component_id):
        self.component_id = component_id

    def register_callback(self, app):
        @app.callback(
            Output('cities-avg-price', 'figure'),
            # Output('cities-avg-graph-container', 'style'),
            Input('filtered-dataset', 'data'),
            Input('filtered-selection', 'data'),
            )
        def update_all_time(filter_data, filter_selections):
            if filter_selections["Municipio"] == []:
                print(f"Cities chart won't be updated! No 'Municipio' was selected.")
                return no_update
            if filter_selections["Produto"] == []:
                print(f"Cities chart won't be updated! No 'Produto' was selected.")
                return no_update
            else:
                # Data preparation
                df = pd.DataFrame.from_dict(filter_data)
                
                city_alltime_avg = df.groupby(["Ano","Municipio"])["Valor de Venda"].agg(["mean"]).reset_index()
                city_alltime_avg_sum = city_alltime_avg.groupby("Municipio")["mean"].agg("sum").reset_index()
                divisor = city_alltime_avg_sum["mean"].max()
                city_alltime_avg["Preço Normalizado"] = city_alltime_avg["mean"].apply(lambda x:x/divisor)
                
                city_order = city_alltime_avg_sum.sort_values("mean", ascending=False)
                city_ordered_list = city_order.set_index("Municipio").index
                city_alltime_avg["Municipio"] = pd.Categorical(city_alltime_avg["Municipio"], categories=city_ordered_list)
                city_alltime_avg['Ano'] = city_alltime_avg['Ano'].astype(str)

                # Figure rendering
                figure = px.bar(
                    city_alltime_avg.sort_values(["Municipio","Ano"], ascending=True),
                    title = "Média anual normalizada de preços nos municipios",
                    x = "Municipio",
                    y = "Preço Normalizado",
                    color = "Ano",
                    color_discrete_sequence=px_colors.qualitative.Plotly
                    
                )
                figure.update_layout(
                    margin = go.layout.Margin(t=50, b=60, l=20),
                    title={
                        'text': "Média anual normalizada de preços nos municipios",
                        'y':0.97, # You can adjust the vertical position (0 to 1)
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                    },
                    autosize=False,
                    height=592
                )
                return figure