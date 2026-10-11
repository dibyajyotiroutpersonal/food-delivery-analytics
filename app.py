
import os
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ---------------------------------------------------------
# 1. Automatic Dataset Finder & Loader
# ---------------------------------------------------------
possible_paths = [
    r"Data\zomato (extracted).csv\zomato.csv",
    r"Data\zomato.csv",
    r"data\zomato.csv",
    "zomato.csv"
]

dataset_path = None
for p in possible_paths:
    if os.path.exists(p):
        dataset_path = p
        break

if dataset_path:
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path, encoding="latin1", on_bad_lines="skip")
    
    # Clean rate column
    if "rate" in df.columns:
        df["rate"] = df["rate"].astype(str).str.split("/").str[0].str.strip()
        df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    
    # Clean cost column
    cost_col = "approx_cost(for two people)" if "approx_cost(for two people)" in df.columns else "cost"
    if cost_col in df.columns:
        df["approx_cost"] = df[cost_col].astype(str).str.replace(",", "").str.strip()
        df["approx_cost"] = pd.to_numeric(df["approx_cost"], errors="coerce")
    
    if "votes" in df.columns:
        df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0)
        
    df = df.dropna(subset=["location", "rate"])
else:
    print("Dataset not found directly. Initializing sample view.")
    np.random.seed(42)
    sample_locs = ["Koramangala", "Indiranagar", "BTM Layout", "Jayanagar", "Whitefield", "HSR Layout"]
    df = pd.DataFrame({
        "name": [f"Restaurant {i}" for i in range(250)],
        "location": np.random.choice(sample_locs, size=250),
        "rate": np.round(np.random.uniform(2.5, 4.9, size=250), 1),
        "approx_cost": np.random.choice([300, 400, 600, 800, 1200, 1500, 2000], size=250),
        "votes": np.random.randint(20, 2500, size=250),
        "online_order": np.random.choice(["Yes", "No"], size=250, p=[0.65, 0.35])
    })

# ---------------------------------------------------------
# 2. Dash UI Layout
# ---------------------------------------------------------
app = Dash(__name__)

available_locations = sorted([str(loc) for loc in df["location"].dropna().unique()])
dropdown_options = [{"label": "All Localities", "value": "ALL"}] + [
    {"label": loc, "value": loc} for loc in available_locations
]

app.layout = html.Div(
    style={"fontFamily": "Segoe UI, Arial, sans-serif", "backgroundColor": "#f8f9fa", "padding": "25px"},
    children=[
        html.Div(
            style={
                "backgroundColor": "#cb202d",
                "padding": "20px",
                "borderRadius": "8px",
                "color": "#ffffff",
                "marginBottom": "20px"
            },
            children=[
                html.H1("Zomato Bangalore Dining & Delivery Analytics", style={"margin": "0"}),
                html.P("Interactive exploration of dining costs, ratings, and locations.", style={"margin": "5px 0 0 0"})
            ]
        ),
        html.Div(
            style={"backgroundColor": "#ffffff", "padding": "15px", "borderRadius": "8px", "marginBottom": "20px"},
            children=[
                html.Label("Select Restaurant Locality:", style={"fontWeight": "600", "display": "block", "marginBottom": "6px"}),
                dcc.Dropdown(
                    id="location-filter",
                    options=dropdown_options,
                    value="ALL",
                    clearable=False,
                    style={"maxWidth": "400px"}
                )
            ]
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                html.Div(
                    style={"backgroundColor": "#ffffff", "padding": "10px", "borderRadius": "8px"},
                    children=[dcc.Graph(id="cost-vs-rating-scatter")]
                ),
                html.Div(
                    style={"backgroundColor": "#ffffff", "padding": "10px", "borderRadius": "8px"},
                    children=[dcc.Graph(id="rating-distribution-hist")]
                )
            ]
        ),
        html.Div(
            style={"backgroundColor": "#ffffff", "padding": "10px", "borderRadius": "8px", "marginTop": "20px"},
            children=[dcc.Graph(id="online-order-cost-box")]
        )
    ]
)

# ---------------------------------------------------------
# 3. Reactive Callbacks
# ---------------------------------------------------------
@app.callback(
    [
        Output("cost-vs-rating-scatter", "figure"),
        Output("rating-distribution-hist", "figure"),
        Output("online-order-cost-box", "figure")
    ],
    [Input("location-filter", "value")]
)
def update_dashboard(selected_location):
    filtered_df = df if selected_location == "ALL" else df[df["location"] == selected_location]
    
    scatter_fig = px.scatter(
        filtered_df,
        x="approx_cost",
        y="rate",
        size="votes" if "votes" in filtered_df.columns else None,
        color="online_order" if "online_order" in filtered_df.columns else None,
        hover_name="name" if "name" in filtered_df.columns else None,
        title=f"Approx Cost vs. Rating ({selected_location})",
        labels={"approx_cost": "Cost for Two (INR)", "rate": "Rating"},
        template="plotly_white"
    )
    
    hist_fig = px.histogram(
        filtered_df,
        x="rate",
        nbins=20,
        marginal="box",
        title=f"Rating Spread ({selected_location})",
        labels={"rate": "Rating"},
        color_discrete_sequence=["#cb202d"],
        template="plotly_white"
    )
    
    box_fig = px.box(
        filtered_df,
        x="online_order" if "online_order" in filtered_df.columns else None,
        y="approx_cost",
        points="outliers",
        title=f"Cost Distribution by Online Ordering ({selected_location})",
        labels={"online_order": "Online Order", "approx_cost": "Cost for Two (INR)"},
        color="online_order" if "online_order" in filtered_df.columns else None,
        template="plotly_white"
    )
    
    return scatter_fig, hist_fig, box_fig

# ---------------------------------------------------------
# 4. Run Application
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
