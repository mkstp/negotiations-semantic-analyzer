import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def plotWPMAirTime(df):
    """
    Plots two graphs:
    1. Words Per Minute (WPM) by ID and Name (Line Chart)
    2. Air Time by ID and Name (Bar Chart)

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        topic_filter (str, optional): Filter the DataFrame by the specified topic.
    """

    # Create a subplot figure
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(
        "WPM by ID and Name (Line Chart)",
        "Air Time by ID and Name (Bar Chart)"
    ))

    # Define a color palette and handle cases where the number of names exceeds the palette length
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    name_list = df["name"].unique()
    color_mapping = {name: colors[i % len(colors)] for i, name in enumerate(name_list)}

    # Add WPM line chart
    for name in name_list:
        filtered_data = df[df["name"] == name]
        fig.add_trace(
            go.Scatter(
                x=filtered_data["id"],
                y=filtered_data["wpm"],
                mode="lines+markers",
                name=f"WPM - {name}",
                line=dict(color=color_mapping[name])
            ),
            row=1,
            col=1
        )

    # Add Air Time bar chart
    for name in name_list:
        filtered_data = df[df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["id"],
                y=filtered_data["airTime"],
                name=f"Air Time - {name}",
                marker_color=color_mapping[name],
            ),
            row=2,
            col=1
        )

    # Update layout for better visualization
    fig.update_layout(
        height=800,  # Increase height to accommodate both graphs
        width=800,   # Adjust width for better visualization
        title_text="WPM (Line) and Air Time (Bar) by ID and Name",
        xaxis=dict(title="ID"),
        xaxis2=dict(title="ID"),
        yaxis=dict(title="WPM"),
        yaxis2=dict(title="Air Time"),
        legend_title="Metrics",
        template="plotly_white"
    )

    fig.show()

def plotNarrativeEmotion(df):

    # Aggregate data to calculate proportions
    proportions = df.groupby(['name', 'nType', 'emotion']).size().reset_index(name='count')
    totals = proportions.groupby(['name', 'nType'])['count'].transform('sum')
    proportions['proportion'] = proportions['count'] / totals

    # Plot stacked bar chart
    fig = px.bar(
        proportions,
        x='nType',
        y='proportion',
        color='emotion',
        barmode='stack',
        facet_col='name',
        title=f"Proportion Emotion by Speaker and Narrative",
        labels={'proportion': 'Proportion', 'nType': 'Narrative', 'emotion': 'Emotion'},
        color_discrete_map={"neutral": "blue", "negative": "red", "positive": "green"},
    )

    # Show plot
    fig.show()

    return fig

def plot_cluster_response_and_coherence(df, legend):
    """
    Creates a scatter plot with linear regression lines for each name.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """
    # Drop rows with missing values for regression
    df = df.dropna(subset=['coherenceScore', 'responseScore'])

    # Group data by name
    grouped = df.groupby('name')

    # Create a scatter plot
    fig = go.Figure()

    for name, group in grouped:
        # Add scatter points
        fig.add_trace(go.Scatter(
            x=group['coherenceScore'],
            y=group['responseScore'],
            mode='markers',
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            text=group['id'],
            hovertemplate="ID: %{text}<br>Coherence Score: %{x}<br>Responsiveness Score: %{y}<extra></extra>"
        ))

        # Perform linear regression if there are enough data points
        if len(group) > 1:
            X = group['coherenceScore'].values.reshape(-1, 1)
            y = group['responseScore'].values
            model = LinearRegression().fit(X, y)
            y_pred = model.predict(X)

            # Add regression line
            fig.add_trace(go.Scatter(
                x=group['coherenceScore'],
                y=y_pred,
                mode='lines',
                name=f"{name} Regression",
                line=dict(color=legend.get(name, 'gray'), dash='dash')
            ))

    # Update layout
    fig.update_layout(
        height=400,
        width=600,
        title="Scatter Plot with Linear Regression Lines",
        xaxis_title="Coherence Score",
        yaxis_title="Responsiveness Score",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        template="plotly_white",
        legend_title="Names"
    )

    return fig

def plot_proportions_response_and_coherence(df, legend):
    """
    Groups the dataframe by 'name' and classifies 'coherenceScore'-'responseScore' pairs
    into four clusters. Displays two subplots:
        1. Proportion of points in each cluster grouped by name.
        2. Average distance of points from the cluster central boundary.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'name', 'coherenceScore', and 'responseScore'.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """

    # Define boundaries for quadrants
    x_boundary = 0.35
    y_boundary = 0.35

    # Map quadrants to cluster labels
    def classify_quadrant(row):
        if row['coherenceScore'] < x_boundary and row['responseScore'] > y_boundary:
            return 'Accommodating'
        elif row['coherenceScore'] < x_boundary:
            return 'Discontinuous'
        elif row['responseScore'] <= y_boundary:
            return 'Directive'
        else:
            return 'Integrative'

    # Classify points into clusters and calculate distances
    df['cluster'] = df.apply(classify_quadrant, axis=1)
    df['distance_to_boundary'] = np.sqrt(
        (df['coherenceScore'] - x_boundary) ** 2 + 
        (df['responseScore'] - y_boundary) ** 2
    )

    # Compute proportions and average distances
    cluster_counts = (
        df.groupby(['name', 'cluster']).size()
        .reset_index(name='count')
    )
    cluster_counts['proportion'] = (
        cluster_counts['count'] / cluster_counts.groupby('name')['count'].transform('sum') * 100
    )
    avg_distances = (
        df.groupby(['name', 'cluster'])['distance_to_boundary']
        .mean().reset_index()
    )

    # Create subplots
    fig = sp.make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            "Proportion of Points in Each Cluster",
            "Average Distance of Clusters to Boundary"
        ],
        vertical_spacing=0.2
    )

    # Add proportion bars
    for name in cluster_counts['name'].unique():
        data = cluster_counts[cluster_counts['name'] == name]
        fig.add_trace(go.Bar(
            x=data['cluster'],
            y=data['proportion'],
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            showlegend=name not in [trace.name for trace in fig.data]  # Avoid duplicate legend entries
        ), row=1, col=1)

    # Add distance bars
    for name in avg_distances['name'].unique():
        data = avg_distances[avg_distances['name'] == name]
        fig.add_trace(go.Bar(
            x=data['cluster'],
            y=data['distance_to_boundary'],
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            showlegend=False  # No additional legend entries needed
        ), row=2, col=1)

    # Update layout and axes
    fig.update_layout(
        height=600,
        width=600,
        title="Cluster Analysis: Proportions and Boundary Distances",
        template="plotly_white",
        showlegend=True
    )
    fig.update_yaxes(title_text="Proportion (%)", row=1, col=1)
    fig.update_yaxes(title_text="Average Distance to Boundary", row=2, col=1)
    fig.update_xaxes(title_text="Cluster", row=1, col=1)
    fig.update_xaxes(title_text="Cluster", row=2, col=1)

    return fig

def plot_frequency_response_and_coherence(df, legend):
    """
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """

    # Determine range for consistent x-axes
    x_range = [0, df['id'].max()]

    # Prepare data for response and coherence charts
    response_df = (
        df.groupby(["name", "responseID"])['responseScore']
        .sum().reset_index(name="resScoreSum")
    )
    coherence_df = (
        df.groupby(["name", "coherenceID"])['coherenceScore']
        .sum().reset_index(name="cohScoreSum")
    )
    coherence_df['cohScoreSum'] *= -1  # Negate coherence scores

    # Create a subplot figure
    fig = sp.make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0
    )

    # Helper function to add traces
    def add_traces(data, y_col, row):
        added_names = set()
        for name in data["name"].unique():
            filtered_data = data[data["name"] == name]
            fig.add_trace(
                go.Bar(
                    x=filtered_data[data.columns[1]],  # responseID or coherenceID
                    y=filtered_data[y_col],
                    name=name,
                    marker=dict(color=legend.get(name, 'gray')),
                    showlegend=name not in added_names
                ),
                row=row, col=1
            )
            added_names.add(name)

    # Add response and coherence traces
    add_traces(response_df, "resScoreSum", row=1)
    add_traces(coherence_df, "cohScoreSum", row=2)

    # Update axes
    for i, title in enumerate(["Response Scores", "Coherence Scores"], start=1):
        fig.update_yaxes(title_text=title, title_standoff=10, row=i, col=1)
        fig.update_xaxes(range=x_range, row=i, col=1)

    # Update layout
    fig.update_layout(
        height=600,
        width=1200,
        barmode='stack',
        template="plotly_white",
        legend_title="Names",
        title="Sum of Responsiveness & Coherence Scores by Name"
    )

    return fig

def plot_repetition(df, legend):
    """
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """

    # Group by name and repeatID for the stacked bar chart
    repeat_df = (
        df.groupby(["name", "repeatID"])["repeatScore"]
        .sum().reset_index(name="repScoreSum")
    )

    # Create a single subplot figure
    fig = sp.make_subplots(rows=1, cols=1, shared_xaxes=True)

    # Add traces for each name
    added_names = set()
    for name in repeat_df["name"].unique():
        filtered_data = repeat_df[repeat_df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["repeatID"],
                y=filtered_data["repScoreSum"],
                name=name,
                marker=dict(color=legend.get(name, 'gray')),  # Use legend for color, fallback to gray
                showlegend=name not in added_names
            )
        )
        added_names.add(name)

    # Update y-axis
    fig.update_yaxes(
        title_text="Repetition Scores",
        title_standoff=10
    )

    # Update layout for better visualization
    fig.update_layout(
        height=400,
        width=1200,
        xaxis=dict(range=[0, df['id'].max()]),
        barmode='stack',
        template="plotly_white",
        legend_title="Names",
        title="Sum of Repeat Scores by Name"
    )

    return fig
