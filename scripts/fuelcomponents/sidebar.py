from dash import callback, Output, Input, html
import plotly.express as px
import dash_bootstrap_components as dbc


# def sidebar():
#     sidebar = dbc.Nav(
#         [
#             dbc.NavItem(dbc.NavLink("Home", href="/")),
#             dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
#             dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
#         ],
#         vertical=True,  # Make it vertical
#         id="sidebar"
#     )
#     return sidebar


# def offcanvas():
#     side_menu_content = html.Div(
#         [
#             html.H2(id="Side Menu", className="display-6 mb-4"),
#             dbc.Nav(
#                 [
#                     dbc.NavLink("Home", href="/", active="exact"),
#                     dbc.NavLink("Page 1", href="/page-1", active="exact"),
#                     dbc.NavLink("Page 2", href="/page-2", active="exact"),
#                     html.Hr(className="my-3"),
#                     html.P("Additional Links", className="text-muted"),
#                     dbc.NavLink("Settings", href="/settings", active="exact"),
#                 ],
#                 vertical=True,
#                 pills=True,
#             ),
#             html.Div(
#                 [
#                     html.P("This menu is always open.", className="mt-4 text-secondary"),
#                     html.P("No close button!", className="text-secondary"),
#                 ],
#                 className="mt-auto" # Pushes content to the bottom if sidebar is tall
#             )
#         ],
#         style={"height": "100%", "display": "flex", "flex-direction": "column"} # Make content fill offcanvas height
#     )
#     test = dbc.Offcanvas(
#         # side_menu_content,
#         id="always-open-sidebar",
#         is_open=True,          # Make it always open
#         backdrop=False,        # Prevent closing when clicking outside
#         close_button=False,    # Remove the close button
#         scrollable=True,       # Allow content to scroll if it's too long
#         placement="start",     # Position it on the left (can be "end" for right)
#         # style=OFFCANVAS_STYLE, # Apply the custom fixed sidebar style
#     )
    
#     return test