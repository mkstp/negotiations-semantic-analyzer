from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

location = 'meetingTranscripts/brady/marc_brady_11-28-2024.json'
location = 'meetingTranscripts/marek/marc_marek_11-06-24.json'

df = pd.read_json(location)

app = Dash()

app.layout = [
    html.Div(className='row', children='My First App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['wpm', 'airTime', 'responseScore', 'efficiency'],
                        value='wpm', 
                        inline=True,
                        id='controls-and-radio-item')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='controls-and-graph')
            ])
    ])
]

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='name', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
