import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc # Still useful for themes and general styling

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) # Using Bootstrap for basic styling

# Define the layout
app.layout = html.Div([
    # This div acts as our simple Navbar
    html.Div(
        [
            html.H3("My Custom Navbar", style={'marginRight': '20px', 'color': 'white'}),
            html.Button('Click Me!', id='navbar-button', n_clicks=0,
                        style={'backgroundColor': '#007bff', 'color': 'white',
                               'border': 'none', 'padding': '10px 15px',
                               'borderRadius': '5px', 'cursor': 'pointer'}),
            html.Div(id='button-click-output', style={'marginLeft': '20px', 'color': 'white'})
        ],
        style={
            'backgroundColor': '#343a40', # Dark background like a navbar
            'padding': '15px 20px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'flex-start',
            'width': '100%' # Occupy full horizontal space
        }
    ),
    html.Hr(),
    html.Div([
        html.H4("Main Content Area"),
        html.P("This is the main content of your application.")
    ], className="p-4") # Some padding for the main content
])

# Define the callback for the button
@callback(
    Output('button-click-output', 'children'),
    Input('navbar-button', 'n_clicks')
)
def update_button_output(n_clicks):
    if n_clicks is None:
        return "" # No clicks yet
    elif n_clicks == 0:
        return "" # Initial state, or perhaps you want to show "Button not clicked yet"
    else:
        return f"Button clicked {n_clicks} time(s)!"

if __name__ == '__main__':
    app.run(debug=True, port=8060)