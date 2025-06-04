from dash import callback, Output, Input, State, html
import dash_bootstrap_components as dbc
from fuelcomponents import offcanvas

right_side = dbc.Row(
    children=[
        dbc.Col(dbc.NavItem(dbc.NavLink("Home", href="/"))),
        # dbc.Col(dbc.NavItem(dbc.NavLink("Sobre", href=None, id="open_modal"))),
        dbc.Col(dbc.Button("Search", color="primary", className="ms-2", n_clicks=0, id="open_modal")),
        dbc.Modal(
            children = [
                dbc.ModalHeader(dbc.ModalTitle("Sobre")),
                dbc.ModalBody("Baseado em *dataset* da Agência Nacional de Petróleo e Gás. [Disponível no Kaggle](https://www.kaggle.com/datasets/paulogladson/anp-combustveis) e generosamente compilado por [Paulo Gladson](https://github.com/PauloGladson)."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_modal", className="ms-auto", n_clicks=0)
                ),
            ], id="modal", is_open=False,
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 1", href="/page1"),
                dbc.DropdownMenuItem("Page 2", href="/page2"),
            ],
            nav=True,
            in_navbar=True,
            label="Mais",
            align_end=True
        ),
    ], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)


def generate_navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            dbc.Button(
                                id="open-offcanvas-scrollable",
                                children=[html.I(className="fa-solid fa-bars")],
                                color="secondary",
                                outline=False, 
                                style={"border-radius":"8px", "height":"40px", "width":"40px"},
                                className="d-flex align-items-center justify-content-center",
                                n_clicks=0,
                            ),
                            width="auto"
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Histórico de preços",
                                # className="ms-2",
                                className="d-flex align-items-center justify-content-center",
                                style={"max-height":"30px"})
                        ),
                    ],
                align="center",
                className="d-flex align-items-center justify-content-center",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    right_side,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True
                ),

                # This is the exact equivalent to right_side
                # dbc.Row(
                #     children=[
                #         dbc.Col(dbc.NavItem(dbc.NavLink("Home", href="/"))),
                #         dbc.Col(dbc.NavItem(dbc.NavLink("Sobre", href="/about"))),
                #         # dbc.DropdownMenu(
                #         #     children=[
                #         #         dbc.DropdownMenuItem("More pages", header=True),
                #         #         dbc.DropdownMenuItem("Page 1", href="/page1"),
                #         #         dbc.DropdownMenuItem("Page 2", href="/page2"),
                #         #     ],
                #         #     nav=True,
                #         #     in_navbar=True,
                #         #     label="Mais",
                #         #     align_end=True
                #         # ),
                #     ], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                # ),


            # Invokes the offcanvas on the offcanvas.py script
            offcanvas.generate_offcanvas()
            ],
        fluid=True,
        style={"min-height":"50px", "max-height":"50px"}
        ),
        # brand="Combustíveis - histórico de preços",
        # brand_href="/",
        color="rgb(50, 56, 62)",
        dark=True,
        fixed="top",  # <<< This makes the navbar fixed at the top
        # className="mb-4", # Add margin-bottom for spacing below the navbar
    # style={"max-height":"50px"}    # 
    )
    return navbar

@callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

# @callback(
#     Output("navbar-collapse", "is_open"),
#     [Input("navbar-toggler", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@callback(
    Output("modal", "is_open"),
    [Input("open_modal", "n_clicks"), Input("close_modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open