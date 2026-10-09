## The Plotly Dash application code

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# If you haven't saved it to a file yet, use the df already in memory:
# Or if loading from disk: df = pd.read_csv('zomato.csv')

# Prepare a clean subset so the dashboard runs fast
dash_df = df[['name', 'location', 'rate', 'cost', 'votes', 'book_table']].dropna().copy()

# Initialize Dash (compatible with Google Colab)
app = Dash(__name__)

# ─── Layout ──────────────────────────────────────
app.layout = html.Div([
    # Header
    html.H1('Food Delivery App Analytics Dashboard (Bangalore)',
            style={'textAlign': 'center', 'color': '#2c3e50',
                   'fontFamily': 'Arial', 'padding': '20px'}),

    # Filter Row
    html.Div([
        html.Label('Select Locality:', style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='location-dropdown',
            options=[{'label': loc, 'value': loc} for loc in sorted(dash_df['location'].unique())],
            value='Koramangala 5th Block' if 'Koramangala 5th Block' in dash_df['location'].values else dash_df['location'].unique()[0],
            style={'width': '350px'}
        )
    ], style={'padding': '15px 25px', 'display': 'flex', 'alignItems': 'center'}),

    # Charts Row
    html.Div([
        dcc.Graph(id='chart-1', style={'flex': 1}),
        dcc.Graph(id='chart-2', style={'flex': 1}),
    ], style={'display': 'flex', 'gap': '15px', 'padding': '0 20px'}),
], style={'backgroundColor': '#f0f2f5', 'minHeight': '100vh', 'fontFamily': 'sans-serif'})

# ─── Callback ──────────────────────────────────
@app.callback(
    [Output('chart-1', 'figure'), Output('chart-2', 'figure')],
    Input('location-dropdown', 'value')
)
def update_charts(selected_location):
    filtered = dash_df[dash_df['location'] == selected_location]

    # Chart 1: Top 10 Rated Restaurants in selected locality
    top_10 = filtered.sort_values(by='rate', ascending=False).head(10)
    fig1 = px.bar(
        top_10,
        x='rate',
        y='name',
        orientation='h',
        title=f'Top Rated Restaurants in {selected_location}',
        color='rate',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'})

    # Chart 2: Cost vs. Rating Scatter Plot
    fig2 = px.scatter(
        filtered,
        x='cost',
        y='rate',
        color='book_table',
        hover_data=['name'],
        title=f'Cost for Two vs. Rating in {selected_location}'
    )
    return fig1, fig2

# ─── Run in Colab ──────────────────────────────
if __name__ == '__main__':
    # jupyter_mode='inline' lets the dashboard render directly inside your Colab notebook
    app.run(jupyter_mode='inline', debug=True)
