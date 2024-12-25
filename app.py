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
            multiple=False
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Dropdown(
        id='topic-filter',
        options=[],
        placeholder='Select a topic',
        style={'width': '50%', 'textAlign': 'center', 'margin': '10px auto'}
    ),

    html.Div([
        dcc.Graph(id='cluster', style={'flex': '1', 'margin': '10px'}),
        dcc.Graph(id='proportions', style={'flex': '1', 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'center'}),


    dcc.Graph(id='frequencies', style={'marginTop': '20px'}),

    html.Div([
        html.H3("Data Table:"),
        dash_table.DataTable(
            id="data-table",
            columns=[],
            data=[],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left",
                "whiteSpace": "normal",
                "height": "auto"
            },
            style_data_conditional=[
                {'if': {'column_id': 'text'}, 'width': '800px', 'whiteSpace': 'normal'},
                {'if': {'column_id': 'name'}, 'width': '100px', 'whiteSpace': 'normal'}
            ]
        )
    ])
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
    [State('upload-data', 'filename')]
)
def update_graph(contents, selected_topic, n_clicks):
    if not contents:
        empty_fig = go.Figure({"layout": {"title": "No Data Available"}})
        return [], empty_fig, empty_fig, empty_fig, [], []  # Match the number of return values

    # Parse uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        error_fig = go.Figure({
            "layout": {
                "title": "Error Parsing File",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return [], error_fig, error_fig, error_fig, [], []  # Match the number of return values

    # Prepare topic filter options
    topic_options = [{'label': topic, 'value': topic} for topic in df['topic'].unique()]

    # Apply topic filter if a topic is selected
    filtered_df = df[df['topic'] == selected_topic] if selected_topic else df

    # Generate the figures using visualizer
    try:
        fig1 = visualizer.plot_cluster_response_and_coherence(filtered_df)
        fig2 = visualizer.plot_proportions_response_and_coherence(filtered_df)
        fig3 = visualizer.plot_frequency_response_and_coherence(filtered_df)
    except Exception as e:
        error_fig = go.Figure({
            "layout": {
                "title": "Error Generating Visualization",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return topic_options, error_fig, error_fig, error_fig, [], []  # Match the number of return values

    # Prepare table data
    required_columns = ['id', 'name', 'text', 'qType', 'nType', 'topic', 'emotion']
    filtered_df = filtered_df[required_columns]
    table_columns = [{"name": col, "id": col} for col in filtered_df.columns]
    table_data = filtered_df.to_dict("records")

    return topic_options, fig1, fig2, fig3, table_columns, table_data

if __name__ == '__main__':
    app.run_server(debug=True)
