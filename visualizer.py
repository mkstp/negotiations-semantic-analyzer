import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

def smooth_scores(data, score_column, window=12, polyorder=2):
    """
    Smooth a score column using the Savitzky-Golay filter.
    If there are not enough points for smoothing, return the raw scores.
    """
    # if len(data) >= window:
    #     return savgol_filter(data[score_column], window_length=window, polyorder=polyorder)
    return data[score_column]

def plotResponsiveCoherence(df, max_id):
    """
    Create two vertically stacked subplots: one for coherence, one for responsiveness.
    """
    df = df[df['id'] <= max_id]
    df_clean = df.dropna(subset=['coherenceScore', 'responsivenessScore'])
    data = df_clean.sort_values(by=["name", "id"])

    smooth_colors = ['purple', 'orange', 'green', 'blue']

    # Initialize subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Smoothed Coherence Scores by Speaker", "Smoothed Responsiveness Scores by Speaker")
    )

    # Plot smoothed coherence scores
    for idx, (name, group) in enumerate(data.groupby('name')):
        smoothed_coherence = smooth_scores(group, 'coherenceScore')
        fig.add_trace(
            go.Scatter(
                x=group['id'],
                y=smoothed_coherence,
                mode='lines',
                line=dict(color=smooth_colors[idx % len(smooth_colors)], width=3),
                name=f'{name} Coherence'
            ),
            row=1, col=1
        )

    # Plot smoothed responsiveness scores
    for idx, (name, group) in enumerate(data.groupby('name')):
        smoothed_responsiveness = smooth_scores(group, 'responsivenessScore')
        fig.add_trace(
            go.Scatter(
                x=group['id'],
                y=smoothed_responsiveness,
                mode='lines',
                line=dict(color=smooth_colors[idx % len(smooth_colors)], width=3, dash='solid'),
                name=f'{name} Responsiveness'
            ),
            row=2, col=1
        )

    fig.update_layout(
        height=800,  # Adjust height to accommodate both graphs
        width=1000,  # Adjust width for better visualization
        showlegend=True,
        title="Smoothed Coherence and Responsiveness Scores by Speaker",
        xaxis_title="ID",
        yaxis_title="Coherence Score",
        yaxis2_title="Responsiveness Score"
    )

    fig.show()

    return fig

def plotEmotionTopic(df):
    # Aggregate data to calculate proportions
    emotion_proportions = df.groupby(['name', 'topic', 'emotion']).size().reset_index(name='count')
    topic_totals = emotion_proportions.groupby(['name', 'topic'])['count'].transform('sum')
    emotion_proportions['proportion'] = emotion_proportions['count'] / topic_totals

    # Plot stacked bar chart
    fig = px.bar(
        emotion_proportions,
        x='topic',
        y='proportion',
        color='emotion',
        barmode='stack',
        facet_col='name',
        title='Proportional Breakdown of Emotion Types by Speaker and Topic',
        labels={'proportion': 'Proportion', 'topic': 'Topic', 'emotion': 'Emotion'},
        color_discrete_map={"neutral": "blue", "negative": "red"}
    )

    # Show plot
    fig.show()

def main():
    # File path and parameters
    file_path = 'marc_marek_11-06-24.json'
    df = pd.read_json(file_path)

    # Create and show plots
    plotResponsiveCoherence(df, 400)
    plotEmotionTopic(df)

# Run the main function
if __name__ == "__main__":
    main()
