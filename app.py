import base64
import io
from dash import Dash, dcc, html, dash_table, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import visualizer

# Initialize the Dash app
app = Dash(__name__)
app.title = "Negotiations Analysis Dashboard"

# Placeholder for data
df = pd.DataFrame()

app.layout = html.Div([
    html.H1("Negotiations Analysis Dashboard", style={'textAlign': 'center'}),

    html.Div([
        # File upload component
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
            style={
                'width': '30%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px auto'
            },
            multiple=False  # Single file upload
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Dropdown(
        id='topic-filter',
        options=[],  # Options will be dynamically set
        placeholder='Select a topic',
        style={'width': '50%'}
    ),

    dcc.Graph(id='cluster'),

    dcc.Graph(id='proportions'),

    # Data table output
    html.Div([
        html.H3("Data Table:"),
        dash_table.DataTable(
            id="data-table",
            columns=[],  # Columns will be dynamically set
            data=[],     # Data will be dynamically set
            page_size=10,  # Display only 10 rows at a time
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left",
                "whiteSpace": "normal",
                "height": "auto"
            },
            style_data_conditional=[
                {
                    'if': {'column_id': 'text'},
                    'width': '800px',
                    'maxWidth': '800px',
                    'minWidth': '200px',
                    'whiteSpace': 'normal',
                },
                {
                    'if': {'column_id': 'name'},
                    'width': '100px',
                    'maxWidth': '100px',
                    'minWidth': '50px',
                    'whiteSpace': 'normal',
                }
            ]
        )
    ]),

    dcc.Graph(id='frequencies')
])

@app.callback(
    [
        Output('topic-filter', 'options'),
        Output('cluster', 'figure'),
        Output('proportions', 'figure'),
        Output('frequencies', 'figure'),
        Output("data-table", "columns"),
        Output("data-table", "data")
    ],
    [
        Input('upload-data', 'contents'),
        Input("topic-filter", "value"), 
    ],
    [
        State('upload-data', 'filename')
    ]
)
def update_graph(contents, selected_topic, n_clicks):
    if not contents:
        # Return placeholders if no file is uploaded
        empty_fig = go.Figure({"layout": {"title": "No Data Available"}})
        return [], empty_fig, empty_fig, empty_fig, [], []

    # Parse uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Assume the uploaded file is a JSON file
        df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        # Handle file parsing errors
        error_fig = go.Figure({
            "layout": {
                "title": "Error Parsing File",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return [], error_fig, error_fig, error_fig, [], []

    # Prepare topic filter options
    topic_options = [{'label': topic, 'value': topic} for topic in df['topic'].unique()]

    # Apply topic filter if a topic is selected
    if selected_topic:
        filtered_df = df[df['topic'] == selected_topic]
    else:
        filtered_df = df

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
        return topic_options, error_fig, error_fig, error_fig, [], []

    # Filter DataFrame to include only required columns
    required_columns = ['id', 'name', 'text', 'qType', 'nType', 'topic', 'emotion']
    filtered_df = filtered_df[required_columns]  # Keep only necessary columns
    filtered_df = filtered_df.loc[:, ~filtered_df.apply(lambda col: col.apply(lambda x: isinstance(x, list)).any())]

    # Prepare table data
    table_columns = [{"name": col, "id": col} for col in filtered_df.columns]
    table_data = filtered_df.to_dict("records")

    # Return updated topic options, figures, and table data
    return topic_options, fig1, fig2, fig3, table_columns, table_data

if __name__ == '__main__':
    app.run_server(debug=True)
