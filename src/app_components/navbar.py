from dash import dcc, callback, Output, Input, State, html
import dash_bootstrap_components as dbc
from .offcanvas import MyOffcanvas

mycanvas = MyOffcanvas("offcanvas-scrollable-class")

class MyNavbar:
    def __init__(self, component_id, output_container_id):
        """
        Initializes the Navbar component.

        Args: 
            component_id (str): The ID for the dbc.Navbar component. This is crucial for callbacks.
            output_container_id (str): The ID of the html.Div component where the output of this dropdown's callback will be displayed.
        """
        self.component_id = component_id
        self.output_container_id = None
        self.right_side = dbc.Row(
            children=[
                dbc.Col(dbc.Button("Sobre", color="primary", n_clicks=0, id="open_modal-class",
                                class_name="g-0 d-flex align-items-center justify-content-center",
                                style={"border-radius":"8px", "height":"40px", "width":"auto"}
                        ), style={"border": "none"}
                ),
                dbc.Col(dbc.NavItem(dbc.NavLink("Contato", href="mailto:azielfreitas@gmail.com" , style={"border": "none"}))),
                dbc.Modal(
                    children = [
                        dbc.ModalHeader(dbc.ModalTitle("Sobre essa visualização...")),
                        dbc.ModalBody(dcc.Markdown("Criada por Aziel Freitas e [dash](https://github.com/plotly/dash).")),
                        dbc.ModalBody(
                            dcc.Markdown("Baseado em *dataset* provido pela Agência Nacional de Petróleo e Gás. [Disponível no Kaggle](https://www.kaggle.com/datasets/paulogladson/anp-combustveis) e generosamente compilado por [Paulo Gladson](https://github.com/PauloGladson).")
                            ),
                        dbc.ModalFooter(
                            dbc.Button("Fechar", id="close_modal-class", className="ms-auto", n_clicks=0)
                        ),
                    ], id="credits-popup", is_open=False, 
                ),
                dbc.Col(
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More pages", header=True),
                            dbc.DropdownMenuItem("Page 1", href="/page1"),
                            dbc.DropdownMenuItem("Page 2", href="/page2"),
                        ],
                        toggle_style={"border": "none"},
                        nav=True,
                        in_navbar=True,
                        label="Mais",
                        align_end=True,

                    )
                )
            ], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", align="center"
        )

    def render(self):
        """
        Renders a dbc.Navbar component within a dbc.Container

        Returns:
            navbar: A fixed bar at the top. Got a sandwich menu and some other buttons.
        """
        navbar = dbc.Navbar(
            id = self.component_id,
            children=[
            dbc.Container(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Button(
                                    id="open-offcanvas",
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
                                    className="d-flex align-items-center justify-content-center",
                                    style={"max-height":"30px", "border":"none"})
                            ),
                        ],
                    align="center",
                    className="d-flex align-items-center justify-content-center",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

                    # dbc.DropdownMenu(
                    #     id="navbar-toggler",
                    #     children=[
                    #         dbc.DropdownMenuItem("More pages", header=True),
                    #         dbc.DropdownMenuItem("Page 1", href="/page1"),
                    #         dbc.DropdownMenuItem("Page 2", href="/page2"),
                    #     ],
                    #     toggle_style={"border": "none"},
                    #     nav=True,
                    #     in_navbar=True,
                    #     label="Mais",
                    #     align_end=True,
                    # ),


                    dbc.Collapse(
                        self.right_side,
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True
                    ),
                # Invokes the offcanvas class
                MyOffcanvas("offcanvas-scrollable-class").render()
                ],
            fluid=True,
            style={"min-height":"50px", "max-height":"50px"}
            ),
            ],
            color="rgb(50, 56, 62)",
            dark=True,
            fixed="top", 
            # className="mb-4", # Add margin-bottom for spacing below the navbar
        # style={"max-height":"50px"}    # 
        )
        return navbar
    
    def register_callbacks(self, app):
        @app.callback(
            Output("offcanvas-scrollable-class", "is_open"),
            Input("open-offcanvas", "n_clicks"),
            State("offcanvas-scrollable-class", "is_open"),
        )
        def toggle_offcanvas_scrollable(n1, is_open):
            if n1:
                return not is_open
            return is_open

        @app.callback(
            Output("credits-popup", "is_open"),
            [
                Input("open_modal-class", "n_clicks"),
                Input("close_modal-class", "n_clicks")
            ],
            State("credits-popup", "is_open"),
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open