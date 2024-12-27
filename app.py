import base64
import io
from dash import Dash, dcc, html, dash_table, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import visualizer
import analyzer

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

    html.Div([
        dcc.Dropdown(
            id='topic-filter',
            options=[],
            placeholder='Filter topic',
            style={'width': '50%', 'margin': '10px'}
        ),
        dcc.Dropdown(
            id='emotion-filter',
            options=[],
            placeholder='Filter emotion',
            style={'width': '50%', 'margin': '10px'}
        ),
        dcc.Dropdown(
            id='ntype-filter',
            options=[],
            placeholder='Filter narrative stance',
            style={'width': '50%', 'margin': '10px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='cluster', style={'flex': '1', 'margin': '10px'}),
        dcc.Graph(id='proportions', style={'flex': '1', 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'center'}),

    dcc.Graph(id='frequencies', style={'marginTop': '20px'}),
    dcc.Graph(id='repetitions', style={'marginTop': '20px'}),

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
        Output('emotion-filter', 'options'),
        Output('ntype-filter', 'options'),
        Output('cluster', 'figure'),
        Output('proportions', 'figure'),
        Output('frequencies', 'figure'),
        Output('repetitions', 'figure'),
        Output("data-table", "columns"),
        Output("data-table", "data")
    ],
    [
        Input('upload-data', 'contents'),
        Input("topic-filter", "value"),
        Input("emotion-filter", "value"),
        Input("ntype-filter", "value")
    ],
    [State('upload-data', 'filename')]
)
def update_graph(contents, selected_topic, selected_emotion, selected_ntype, filename):
    if not contents:
        empty_fig = go.Figure({"layout": {"title": "No Data Available"}})
        return [], [], [], empty_fig, empty_fig, empty_fig, empty_fig, [], []

    # Parse uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        global df
        if filename.endswith('.txt'):
            # Analyze .txt file
            df = analyzer.analyzeTranscript(decoded.decode('utf-8'), filename)
        elif filename.endswith('.json'):
            # Read JSON file
            df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
        else:
            raise ValueError("Unsupported file format. Please upload a Fathom transcript .txt or a preprocessed .json file.")
    except Exception as e:
        error_fig = go.Figure({
            "layout": {
                "title": "Error Parsing File",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return [], [], [], error_fig, error_fig, error_fig, error_fig, [], []

    # Prepare filter options
    topic_options = [{'label': topic, 'value': topic} for topic in df['topic'].unique()]
    emotion_options = [{'label': emotion, 'value': emotion} for emotion in df['emotion'].unique()]
    ntype_options = [{'label': ntype, 'value': ntype} for ntype in df['nType'].unique()]

    # Apply filters
    filtered_df = df
    if selected_topic:
        filtered_df = filtered_df[filtered_df['topic'] == selected_topic]
    if selected_emotion:
        filtered_df = filtered_df[filtered_df['emotion'] == selected_emotion]
    if selected_ntype:
        filtered_df = filtered_df[filtered_df['nType'] == selected_ntype]

    # Create a legend dictionary with unique 'name' values mapped to colors
    unique_names = filtered_df['name'].unique()
    colors = ['blue', 'red']
    legend = {name: colors[i % len(colors)] for i, name in enumerate(unique_names)}

    # Generate the figures using visualizer with the legend passed
    try:
        fig1 = visualizer.plot_cluster_response_and_coherence(filtered_df, legend)
        fig2 = visualizer.plot_proportions_response_and_coherence(filtered_df, legend)
        fig3 = visualizer.plot_frequency_response_and_coherence(filtered_df, legend)
        fig4 = visualizer.plot_repetition(filtered_df, legend)
    except Exception as e:
        error_fig = go.Figure({
            "layout": {
                "title": "Error Generating Visualization",
                "annotations": [{"text": str(e), "showarrow": False}]
            }
        })
        return topic_options, emotion_options, ntype_options, error_fig, error_fig, error_fig, error_fig, [], []

    # Prepare table data
    required_columns = ['id', 'name', 'text', 'responseID', 'coherenceID', 'repeatID']
    filtered_df = filtered_df[required_columns]
    table_columns = [{"name": col, "id": col} for col in filtered_df.columns]
    table_data = filtered_df.to_dict("records")

    return topic_options, emotion_options, ntype_options, fig1, fig2, fig3, fig4, table_columns, table_data

if __name__ == '__main__':
    app.run_server(debug=True)
