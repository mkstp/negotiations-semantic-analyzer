import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

def load_and_clean_data(file_path, max_id):
    """
    Load JSON data, filter by max ID, and clean NaN values.
    """
    df = pd.read_json(file_path)
    df = df[df['id'] <= max_id]
    df_clean = df.dropna(subset=['coherenceScore', 'responsivenessScore'])
    return df_clean.sort_values(by=["name", "id"])

def smooth_scores(data, score_column, window=12, polyorder=2):
    """
    Smooth a score column using the Savitzky-Golay filter.
    If there are not enough points for smoothing, return the raw scores.
    """
    if len(data) >= window:
        return savgol_filter(data[score_column], window_length=window, polyorder=polyorder)
    return data[score_column]

def create_subplots(data, smooth_colors):
    """
    Create two vertically stacked subplots: one for coherence, one for responsiveness.
    """
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

    return fig

def customize_and_show(fig):
    """
    Customize the layout of the subplots and display the figure.
    """
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

def main():
    # File path and parameters
    file_path = 'marc_marek_11-06-24.json'
    max_id = 400
    smooth_colors = ['purple', 'orange', 'green', 'blue']

    # Load and clean data
    df_clean = load_and_clean_data(file_path, max_id)

    # Create and show plots
    fig = create_subplots(df_clean, smooth_colors)
    customize_and_show(fig)

# Run the main function
if __name__ == "__main__":
    main()
