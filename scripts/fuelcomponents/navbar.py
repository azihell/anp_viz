from dash import callback, Output, Input, State, html
import dash_bootstrap_components as dbc
from fuelcomponents import offcanvas

offcanvass = html.Div(
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


def generate_navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            children=[
                dbc.Row([
                    dbc.Col(
                        dbc.Button(
                            children=[
                                html.Img(
                                    src="/assets/menu-bar-icon.png",
                                   style={"max-height":"30px"},  # Adjust image height as needed
                                    # className="me-2", # Add some margin to the right of the image
                                ),
                                # "Download", # You can still have text next to the image
                            ],
                                id="open-offcanvas-scrollable",
                                n_clicks=0,
                                outline=False, 
                                color="secondary",
                                className="p-0 m-0",
                                style={"border-radius":"10px"}
                                ),
                    width="auto"),
                    dbc.Col(dbc.NavbarBrand("Histórico de preços", className="ms-2", style={"max-height":"30px"})),
                    ], align="center", className="g-0"
                ),
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Sobre", href="/about")),
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
            # offcanvas
            offcanvas.generate_offcanvas()
            ],
        fluid=True,
        style={"min-height":"40px", "max-height":"40px"}
        ),
        # brand="Combustíveis - histórico de preços",
        # brand_href="/",
        color="rgb(50, 56, 62)",
        dark=True,
        fixed="top",  # <<< This makes the navbar fixed at the top
        # className="mb-4", # Add margin-bottom for spacing below the navbar
    style={"max-height":"50px"} )
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