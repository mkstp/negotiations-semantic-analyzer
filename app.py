import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import visualizer

# Initialize the Dash app
app = Dash(__name__)
app.title = "Negotiations Analysis Dashboard"

# Placeholder for data
df = pd.DataFrame()

fileName = 'meetingTranscripts/negotiation_roleplay/d_marc_2_12-19-2024.json'
df = pd.read_json(fileName)

app.layout = html.Div([
    html.H1("Negotiations Analysis Dashboard", style={'textAlign': 'center'}),
    html.Div([
        # Input for file location
        dcc.Input(
            id="location", 
            type="text", 
            placeholder="Enter file location", 
            debounce=True,
            style={'width': '30%'}
        ),
        dcc.Dropdown(
            id='topic-filter',
            options=[{'label': topic, 'value': topic} for topic in df['topic'].unique()],
            placeholder='Select a topic',
            style={'width': '50%'}
        ),
        # Submit button
        html.Button(
            "Generate Chart", 
            id="submit-button", 
            n_clicks=0
        ),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Data table output
    html.Div([
        html.H3("Underlying Data Table:"),
        dash_table.DataTable(
            id="data-table",
            columns=[],  # Columns will be dynamically set
            data=[],     # Data will be dynamically set
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"}
        )
    ]),

    dcc.Graph(id='frequencies'),
    dcc.Graph(id='cluster'),
    dcc.Graph(id='proportions')
])

@app.callback(
    [    
        Output('frequencies', 'figure'),
        Output('cluster', 'figure'),
        Output('proportions', 'figure'),
        Output("data-table", "columns"),
        Output("data-table", "data")
    ],
    [
        Input('topic-filter', 'value'),
        Input("submit-button", "n_clicks")
    ],
    [
        State("location", "value"),
        State("topic-filter", "value")
    ]
)

def update_graph(topic_filter, n_clicks, location, state_topic_filter):

    if not location:
        # Return placeholders if no file location is provided
        empty_fig = go.Figure({"layout": {"title": "No Data Available"}})
        return empty_fig, empty_fig, empty_fig, [], []

    # Attempt to load data from the specified location
    try:
        df = pd.read_json(location)
    except Exception as e:
        # Handle file loading errors
        error_fig = go.Figure({
            "layout": {
                "title": "Error Loading Data",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return error_fig, error_fig, error_fig, [], []
    
    # Filter the DataFrame by topic if provided
    filtered_df = df if not topic_filter else df[df['topic'] == topic_filter]

    # Prepare table data
    filtered_df = filtered_df.loc[:, ~filtered_df.apply(lambda col: col.apply(lambda x: isinstance(x, list)).any())]
    table_columns = [{"name": col, "id": col} for col in filtered_df.columns]
    table_data = filtered_df.to_dict("records")

    # Generate the figures using visualizer
    try:
        fig1 = visualizer.plot_cluster_response_and_coherence(filtered_df)
        fig2 = visualizer.plot_proportions_response_and_coherence(filtered_df)
        fig3 = visualizer.plot_frequency_response_and_coherence(filtered_df)
        
    except Exception as e:
        # Handle errors from visualizer functions
        error_fig = go.Figure({
            "layout": {
                "title": "Error Generating Visualization",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return error_fig, error_fig, table_columns, table_data

    # Return the generated figures and table data
    return fig1, fig2, fig3, table_columns, table_data

if __name__ == '__main__':
    app.run_server(debug=True)
