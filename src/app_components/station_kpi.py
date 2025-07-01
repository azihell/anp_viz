from dash import dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Sample data for our KPI

class StationsKPI:
    def __init__(self, component_id):
        self.component_id = component_id
 
    def register_callback(self, app):
        @app.callback(
            Output("station_kpi","figure"),
            Input('filtered-dataset', 'data')
        )
        def update_kpi(data):
            df = pd.DataFrame.from_dict(data)
            earliest_year = df["Ano"].unique().tolist()[0]
            latest_year = df["Ano"].unique().tolist()[-1]
            earliest_check = df["Ano"] == earliest_year
            latest_check = df["Ano"] == latest_year
            earliest_unique_count = df[earliest_check]["CNPJ da Revenda"].nunique()
            latest_unique_count = df[latest_check]["CNPJ da Revenda"].nunique()
            kpi_figure = go.Figure(
                go.Indicator(
                    mode="number+delta",  # Show both the number and the delta
                    value=earliest_unique_count,
                    number={
                        "prefix": "Ano final: ",
                        "valueformat": ".0f",  # Format as currency with comma separators
                        "font": {"size": 20}
                        },
                    delta={
                        "prefix": " Ano inicial: ",
                        "reference": latest_unique_count,
                        "valueformat": ".2%",
                        "relative": True,  # Show absolute change, not percentage
                        "position": "bottom", # Position the delta below the number
                        "increasing": {"color": "green"}, # Color for positive change
                        "decreasing": {"color": "red"},   # Color for negative change
                        "font": {"size": 15}
                    },
                )
            )
            kpi_figure.update_layout(height=100, margin=dict(l=10, r=10, t=10, b=10))
            return kpi_figure
