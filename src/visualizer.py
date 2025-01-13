"""
Marc St. Pierre 1/13/2025
This module contains functions to generate the plots that display conversational data in the app
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from sklearn.linear_model import LinearRegression


def plot_wpma_air_time(df, legend):
    """
    Plots two graphs:
    1. Words Per Minute (WPM) by ID and Name (Line Chart)
    2. Air Time by ID and Name (Bar Chart)

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """
    fig = sp.make_subplots(
        rows=2, cols=1, shared_xaxes=True, 
        subplot_titles=(
            "WPM by ID and Name (Line Chart)",
            "Air Time by ID and Name (Bar Chart)"
        )
    )

    name_list = df["name"].unique()

    for name in name_list:
        filtered_data = df[df["name"] == name]
        fig.add_trace(
            go.Scatter(
                x=filtered_data["id"],
                y=filtered_data["wpm"],
                mode="lines+markers",
                name=f"WPM - {name}",
                line=dict(color=legend.get(name, 'gray'))
            ),
            row=1, col=1
        )

    for name in name_list:
        filtered_data = df[df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["id"],
                y=filtered_data["airTime"],
                name=f"Air Time - {name}",
                marker_color=legend.get(name, 'gray'),
            ),
            row=2, col=1
        )

    fig.update_layout(
        height=800,
        width=800,
        title_text="WPM (Line) and Air Time (Bar) by ID and Name",
        xaxis=dict(title="ID"),
        xaxis2=dict(title="ID"),
        yaxis=dict(title="WPM"),
        yaxis2=dict(title="Air Time"),
        legend_title="Metrics",
        template="plotly_white"
    )

    return fig


def plot_narrative_emotion(df, legend):
    """
    Plots a stacked bar chart of emotion proportions by speaker and narrative type.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'emotion' values to consistent colors.
    """
    proportions = df.groupby(['name', 'nType', 'emotion']).size().reset_index(name='count')
    totals = proportions.groupby(['name', 'nType'])['count'].transform('sum')
    proportions['proportion'] = proportions['count'] / totals

    fig = px.bar(
        proportions,
        x='nType',
        y='proportion',
        color='emotion',
        barmode='stack',
        facet_col='name',
        title="Proportion Emotion by Speaker and Narrative",
        labels={'proportion': 'Proportion', 'nType': 'Narrative', 'emotion': 'Emotion'},
        color_discrete_map=legend,
    )

    return fig


def plot_cluster_response_and_coherence(df, legend):
    """
    Creates a scatter plot with linear regression lines for each name.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """
    df = df.dropna(subset=['coherenceScore', 'responseScore'])
    grouped = df.groupby('name')

    fig = go.Figure()

    for name, group in grouped:
        fig.add_trace(go.Scatter(
            x=group['coherenceScore'],
            y=group['responseScore'],
            mode='markers',
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            text=group['id'],
            hovertemplate="ID: %{text}<br>Coherence Score: %{x}<br>Responsiveness Score: %{y}<extra></extra>"
        ))

        if len(group) > 1:
            X = group['coherenceScore'].values.reshape(-1, 1)
            y = group['responseScore'].values
            model = LinearRegression().fit(X, y)
            y_pred = model.predict(X)

            fig.add_trace(go.Scatter(
                x=group['coherenceScore'],
                y=y_pred,
                mode='lines',
                name=f"{name} Regression",
                line=dict(color=legend.get(name, 'gray'), dash='dash')
            ))

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
    x_boundary, y_boundary = 0.35, 0.35

    def classify_quadrant(row):
        if row['coherenceScore'] < x_boundary and row['responseScore'] > y_boundary:
            return 'Accommodating'
        elif row['coherenceScore'] < x_boundary:
            return 'Discontinuous'
        elif row['responseScore'] <= y_boundary:
            return 'Directive'
        return 'Integrative'

    df['cluster'] = df.apply(classify_quadrant, axis=1)
    df['distance_to_boundary'] = np.sqrt(
        (df['coherenceScore'] - x_boundary) ** 2 +
        (df['responseScore'] - y_boundary) ** 2
    )

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

    fig = sp.make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            "Proportion of Points in Each Cluster",
            "Average Distance of Clusters to Boundary"
        ],
        vertical_spacing=0.2
    )

    for name in cluster_counts['name'].unique():
        data = cluster_counts[cluster_counts['name'] == name]
        fig.add_trace(go.Bar(
            x=data['cluster'],
            y=data['proportion'],
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            showlegend=name not in [trace.name for trace in fig.data]
        ), row=1, col=1)

    for name in avg_distances['name'].unique():
        data = avg_distances[avg_distances['name'] == name]
        fig.add_trace(go.Bar(
            x=data['cluster'],
            y=data['distance_to_boundary'],
            name=name,
            marker=dict(color=legend.get(name, 'gray')),
            showlegend=False
        ), row=2, col=1)

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
    Plots stacked bar charts of response and coherence scores grouped by name.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """
    x_range = [0, df['id'].max()]

    response_df = (
        df.groupby(["name", "responseID"])['responseScore']
        .sum().reset_index(name="resScoreSum")
    )
    coherence_df = (
        df.groupby(["name", "coherenceID"])['coherenceScore']
        .sum().reset_index(name="cohScoreSum")
    )
    coherence_df['cohScoreSum'] *= -1

    fig = sp.make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0
    )

    def add_traces(data, y_col, row):
        added_names = set()
        for name in data["name"].unique():
            filtered_data = data[data["name"] == name]
            fig.add_trace(
                go.Bar(
                    x=filtered_data[data.columns[1]],
                    y=filtered_data[y_col],
                    name=name,
                    marker=dict(color=legend.get(name, 'gray')),
                    showlegend=name not in added_names
                ),
                row=row, col=1
            )
            added_names.add(name)

    add_traces(response_df, "resScoreSum", row=1)
    add_traces(coherence_df, "cohScoreSum", row=2)

    for i, title in enumerate(["Response Scores", "Coherence Scores"], start=1):
        fig.update_yaxes(title_text=title, title_standoff=10, row=i, col=1)
        fig.update_xaxes(range=x_range, row=i, col=1)

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
    Plots repetition scores grouped by name and repeatID.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        legend (dict): Dictionary mapping 'name' values to consistent colors.
    """
    repeat_df = (
        df.groupby(["name", "repeatID"])["repeatScore"]
        .sum().reset_index(name="repScoreSum")
    )

    fig = sp.make_subplots(rows=1, cols=1, shared_xaxes=True)

    added_names = set()
    for name in repeat_df["name"].unique():
        filtered_data = repeat_df[repeat_df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["repeatID"],
                y=filtered_data["repScoreSum"],
                name=name,
                marker=dict(color=legend.get(name, 'gray')),
                showlegend=name not in added_names
            )
        )
        added_names.add(name)

    fig.update_yaxes(title_text="Repetition Scores", title_standoff=10)

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