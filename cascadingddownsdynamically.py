import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State

# Sample Data: This DataFrame represents your raw data
# In a real application, this might come from a database, CSV, API, etc.
data = {
    'City': ['New York', 'New York', 'New York', 'Los Angeles', 'Los Angeles', 'Chicago', 'Chicago', 'Chicago', 'New York', 'Los Angeles'],
    'Category': ['Electronics', 'Electronics', 'Books', 'Electronics', 'Books', 'Books', 'Home', 'Electronics', 'Home', 'Electronics'],
    'Product': ['Laptop', 'Smartphone', 'Novel', 'Laptop', 'Comic Book', 'Novel', 'Couch', 'Tablet', 'Lamp', 'TV'],
    'Price': [1200, 800, 15, 1100, 10, 20, 800, 700, 50, 900],
    'Stock': [10, 25, 50, 5, 30, 20, 5, 15, 100, 12]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div(
    className="min-h-screen bg-gray-100 p-8 flex flex-col items-center justify-center font-inter",
    children=[
        html.H1(
            "Dynamic Filtering with Cascading Dropdowns",
            className="text-4xl font-bold text-gray-800 mb-8 rounded-lg p-4 bg-white shadow-lg"
        ),
        html.Div(
            className="bg-white p-8 rounded-lg shadow-xl w-full max-w-lg grid grid-cols-1 gap-6",
            children=[
                html.Div(
                    children=[
                        html.Label("Select City:", className="block text-gray-700 text-lg font-semibold mb-2"),
                        dcc.Dropdown(
                            id='city-dropdown',
                            options=[{'label': i, 'value': i} for i in df['City'].unique()],
                            placeholder="Select a city",
                            className="rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500",
                            clearable=True # Allow clearing selection
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Select Category:", className="block text-gray-700 text-lg font-semibold mb-2"),
                        dcc.Dropdown(
                            id='category-dropdown',
                            options=[], # Initially empty
                            placeholder="Select a category",
                            className="rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500",
                            clearable=True
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Select Product:", className="block text-gray-700 text-lg font-semibold mb-2"),
                        dcc.Dropdown(
                            id='product-dropdown',
                            options=[], # Initially empty
                            placeholder="Select a product",
                            className="rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500",
                            clearable=True
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id='selection-output',
            className="mt-8 p-4 bg-blue-100 text-blue-800 rounded-lg shadow-md w-full max-w-lg text-center"
        )
    ]
)

# Callback to update Category options based on City selection
@app.callback(
    Output('category-dropdown', 'options'),
    Output('category-dropdown', 'value'), # Also output to clear the value
    Output('product-dropdown', 'options'), # Also clear product options
    Output('product-dropdown', 'value'),   # Also clear product value
    Input('city-dropdown', 'value')
)
def update_category_options(selected_city):
    # If no city is selected, return empty options for category and product, and clear their values
    if selected_city is None:
        return [], None, [], None

    # Filter the DataFrame based on the selected city
    filtered_df = df[df['City'] == selected_city]

    # Get unique categories from the filtered data
    categories = [{'label': i, 'value': i} for i in filtered_df['Category'].unique()]

    # When city changes, categories and products should reset
    return categories, None, [], None

# Callback to update Product options based on City and Category selections
@app.callback(
    Output('product-dropdown', 'options'),
    Output('product-dropdown', 'value'), # Also output to clear the value
    Input('city-dropdown', 'value'),
    Input('category-dropdown', 'value')
)
def update_product_options(selected_city, selected_category):
    # If either city or category is not selected, return empty options and clear product value
    if selected_city is None or selected_category is None:
        return [], None

    # Filter the DataFrame based on both selected city and category
    filtered_df = df[(df['City'] == selected_city) & (df['Category'] == selected_category)]

    # Get unique products from the further filtered data
    products = [{'label': i, 'value': i} for i in filtered_df['Product'].unique()]

    # When category changes (or city, due to upstream trigger), products should reset
    return products, None

# Callback to display the final selections
@app.callback(
    Output('selection-output', 'children'),
    Input('city-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('product-dropdown', 'value')
)
def display_selections(city, category, product):
    return f"Selected: City: {city if city else 'None'}, Category: {category if category else 'None'}, Product: {product if product else 'None'}"


if __name__ == '__main__':
    app.run_server(debug=True)

