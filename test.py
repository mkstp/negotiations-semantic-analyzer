import plotly.express as px
import pandas as pd
from scipy.signal import savgol_filter

file_path = 'marc_marek_11-06-24.json'
df = pd.read_json(file_path)

datay = savgol_filter(df['coherenceScore'], window_length=7, polyorder=2)

data2 = savgol_filter(df['responseScore'], window_length=7, polyorder=2)


fig1 = px.line(df, x="id", y=df['coherenceScore'], title='Coherence', color='name')
fig2 = px.line(df, x="id", y=df['responseScore'], title='Responsiveness', color='name')

fig1.update_layout(
    height=500,  # Adjust height to accommodate both graphs
    width=1000,  # Adjust width for better visualization
    showlegend=True,
    title="Smoothed Coherence Scores by Speaker",
    xaxis_title="ID",
    yaxis_title="Coherence Score",
)

fig2.update_layout(
    height=500,  # Adjust height to accommodate both graphs
    width=1000,  # Adjust width for better visualization
    showlegend=True,
    title="Smoothed Responsiveness Scores by Speaker",
    xaxis_title="ID",
    yaxis_title="Responsiveness Score",
)

fig1.show()
fig2.show()