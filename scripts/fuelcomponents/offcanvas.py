import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

# def generate_offcanvas():
#     offcanvas = dbc.Offcanvas(
#         html.P("The contents on the main page are now scrollable."),
#         id="offcanvas-scrollable",
#         scrollable=True,
#         title="Scrollable Offcanvas",
#         is_open=False,
#     ),
#     return offcanvas

def generate_offcanvas():
    offcanvas = html.Div(
        [
            dbc.Offcanvas(
                html.P("The contents on the main page are now scrollable."),
                id="offcanvas-scrollable",
                scrollable=True,
                title="Scrollable Offcanvas",
                is_open=False,
            ),
        ]
    )
    return offcanvas