import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def plotWPMAirTime(df, topic_filter=None):
    """
    Plots two graphs:
    1. Words Per Minute (WPM) by ID and Name (Line Chart)
    2. Air Time by ID and Name (Bar Chart)

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        topic_filter (str, optional): Filter the DataFrame by the specified topic.
    """
    # Optionally filter the DataFrame by topic
    if topic_filter:
        df = df[df['topic'] == topic_filter]

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

def plot_cluster_response_and_coherence(df):
    
    # Group the data by name
    grouped = df.groupby('name')

    # Create a scatter plot
    fig = go.Figure()

    colors_points = ['blue', 'red']  # Colors for the scatter points
    colors_lines = ['cyan', 'orange']  # Colors for the regression lines
    
    for idx, (name, group) in enumerate(grouped):

        # Drop NaN values for the regression analysis
        group = group.dropna(subset=['coherenceScore', 'responseScore'])

        # Add scatter points for each name
        fig.add_trace(go.Scatter(
            x=group['coherenceScore'],
            y=group['responseScore'],
            mode='markers',
            name=f'{name} - Points',
            marker=dict(color=colors_points[idx % len(colors_points)]),  # Cycle through the point colors
            text=group['id'],  # Display ID on hover
            hovertemplate="ID: %{text}<br>Coherence Score: %{x}<br>Responsiveness Score: %{y}<extra></extra>"
        ))

        # Perform linear regression
        X = group['coherenceScore'].values.reshape(-1, 1)
        y = group['responseScore'].values
        if len(X) > 1:  # Ensure there are enough points for regression
            model = LinearRegression().fit(X, y)
            y_pred = model.predict(X)

            # Add the regression line for each name
            fig.add_trace(go.Scatter(
                x=group['coherenceScore'],
                y=y_pred,
                mode='lines',
                name=f'{name} - Regression Line',
                line=dict(color=colors_lines[idx % len(colors_lines)])  # Cycle through the line colors
            ))

    # Update the layout for better visualization
    fig.update_layout(
        height=500,  # Adjust height to accommodate both graphs
        width=800,  # Adjust width for better visualization
        title=f"Scatter Plot with Linear Regression Lines",
        xaxis_title="Coherence Score",
        yaxis_title="Responsiveness Score",
        legend_title="Names",
        template="plotly_white"
    )

    return fig

def plot_proportions_response_and_coherence(df):
    """
    Groups the dataframe by 'name' and classifies 'coherenceScore'-'responseScore' pairs
    into four clusters (Accommodating, Discontinuous, Directive, Integrative). 
    Displays two subplots:
        1. Proportion of points in each cluster grouped by name.
        2. Average distance of points from the cluster central boundary (x_boundary, y_boundary).

    Parameters:
        df (pd.DataFrame): DataFrame containing 'name', 'coherenceScore', and 'responseScore'.
    """

    # Ensure the required columns exist
    if not {'name', 'coherenceScore', 'responseScore'}.issubset(df.columns):
        raise ValueError("The DataFrame must contain 'name', 'coherenceScore', and 'responseScore' columns.")

    # Define boundaries for quadrants
    x_boundary = 0.35
    y_boundary = 0.35

    # Map quadrants to cluster labels
    def classify_quadrant(row):
        if row['coherenceScore'] < x_boundary and row['responseScore'] > y_boundary:
            return 'Accommodating'
        elif row['coherenceScore'] < x_boundary and row['responseScore'] <= y_boundary:
            return 'Discontinuous'
        elif row['coherenceScore'] >= x_boundary and row['responseScore'] <= y_boundary:
            return 'Directive'
        else:
            return 'Integrative'

    # Apply classification to each row
    df['cluster'] = df.apply(classify_quadrant, axis=1)

    # Compute proportions for the first subplot
    cluster_counts = df.groupby(['name', 'cluster']).size().reset_index(name='count')
    total_points = cluster_counts.groupby('name')['count'].transform('sum')
    cluster_counts['proportion'] = cluster_counts['count'] / total_points

    # Calculate distances to the central boundary
    def calculate_distance(row):
        return np.sqrt((row['coherenceScore'] - x_boundary) ** 2 + (row['responseScore'] - y_boundary) ** 2)

    df['distance_to_boundary'] = df.apply(calculate_distance, axis=1)

    # Compute average distances grouped by name and cluster
    avg_distances = df.groupby(['name', 'cluster'])['distance_to_boundary'].mean().reset_index()

    # Define consistent colors for each name
    unique_names = df['name'].unique()
    color_palette = px.colors.qualitative.Plotly
    name_colors = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

    # Create subplots
    fig = sp.make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            "Proportion of Points in Each Cluster",
            "Average Distance of Point Clusters to Boundary Center"
        ],
        vertical_spacing=0.2
    )

    # Add the first subplot (Proportions)
    for name in cluster_counts['name'].unique():
        name_data = cluster_counts[cluster_counts['name'] == name]
        fig.add_trace(
            go.Bar(
                x=name_data['cluster'],
                y=name_data['proportion'] * 100,  # Convert to percentage
                name=name,
                marker=dict(color=name_colors[name]),
                showlegend=True if name not in fig['data'] else False  # Avoid duplicate names
            ),
            row=1, col=1
        )

    # Add the second subplot (Average Distances)
    for name in avg_distances['name'].unique():
        name_data = avg_distances[avg_distances['name'] == name]
        fig.add_trace(
            go.Bar(
                x=name_data['cluster'],
                y=name_data['distance_to_boundary'],
                name=name,
                marker=dict(color=name_colors[name]),
                showlegend=False  # Avoid duplicate legend entries
            ),
            row=2, col=1
        )

    # Update layout
    fig.update_layout(
        height=600,
        title_text="Cluster Analysis: Proportions and Boundary Distances",
        template="plotly_white",
        showlegend=True
    )

    # Update axes
    fig.update_yaxes(title_text="Proportion (%)", range=[0, 100], row=1, col=1)
    fig.update_yaxes(title_text="Average Distance to Boundary", row=2, col=1)
    fig.update_xaxes(title_text="Cluster", row=1, col=1)
    fig.update_xaxes(title_text="Cluster", row=2, col=1)

    return fig

def plotNarrativeEmotion(df, topic_filter=None):

    # Optionally filter the DataFrame by topic
    if topic_filter:
        df = df[df['topic'] == topic_filter]

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
        title=f"Proportion Emotion by Speaker and Narrative{' for ' + topic_filter if topic_filter else ''}",
        labels={'proportion': 'Proportion', 'nType': 'Narrative', 'emotion': 'Emotion'},
        color_discrete_map={"neutral": "blue", "negative": "red", "positive": "green"},
    )

    # Show plot
    fig.show()

    return fig

def plot_frequency_response_and_coherence(df):
    """
    Creates three frequency histograms and their respective line graphs for average scores:
    1. Frequency of ResponseIDs grouped by name and Average Response Scores.
    2. Frequency of CoherenceIDs grouped by name and Average Coherence Scores.
    3. Frequency of RepeatIDs grouped by name (stacked bars) and Average Repeat Scores grouped by name.

    Histograms and line graphs are displayed in a single figure with subplots.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
    """

    # Determine range for consistent x-axes
    x_range = [0, df['id'].max()]

    # Group by name and responseID for bar chart frequency
    freq_response_df = df.groupby(["name", "responseID"]).size().reset_index(name="frequency")
    score_response_df = df.groupby("responseID")["responseScore"].mean().reset_index()

    # Group by name and coherenceID for bar chart frequency
    freq_coherence_df = df.groupby(["name", "coherenceID"]).size().reset_index(name="frequency")
    score_coherence_df = df.groupby("coherenceID")["coherenceScore"].mean().reset_index()

    # Group by name and repeatID for bar chart frequency
    freq_repeat_df = df.groupby(["name", "repeatID"]).size().reset_index(name="frequency")
    score_repeat_df = df.groupby(["name", "repeatID"])["repeatScore"].mean().reset_index()

    # Generate consistent color mapping for names
    unique_names = df["name"].unique()
    color_palette = px.colors.qualitative.Plotly  # Use Plotly's default qualitative palette
    color_mapping = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

    # Create a subplot figure with 3 rows and 2 columns
    fig = sp.make_subplots(
        rows=3, cols=2, shared_xaxes=True, 
        subplot_titles=(
            "ResponseIDs by Name",
            "Average Response Scores by ResponseID",
            "CoherenceIDs by Name",
            "Average Coherence Scores by CoherenceID",
            "RepeatIDs by Name (Stacked)",
            "Average Repeat Scores by RepeatID (Grouped by Name)"
        ),
        vertical_spacing=0.15  # Reduce vertical spacing between rows
    )

    # Keep track of which names have already been added to the legend
    names_in_legend = set()

    # 1. Add ResponseID bar chart (left column)
    for name in freq_response_df["name"].unique():
        filtered_data = freq_response_df[freq_response_df["name"] == name]
        show_legend = name not in names_in_legend
        fig.add_trace(
            go.Bar(
                x=filtered_data["responseID"],
                y=filtered_data["frequency"],
                name=name,
                marker=dict(color=color_mapping[name]),
                showlegend=show_legend
            ),
            row=1,
            col=1
        )
        names_in_legend.add(name)

    # 2. Add Response Score Average Line Graph (right column)
    fig.add_trace(
        go.Scatter(
            x=score_response_df["responseID"],
            y=score_response_df["responseScore"],
            mode='lines',
            name="Average Response Score",
            line=dict(color="black", width=1)
        ),
        row=1,
        col=2
    )

    # 3. Add CoherenceID bar chart (left column)
    for name in freq_coherence_df["name"].unique():
        filtered_data = freq_coherence_df[freq_coherence_df["name"] == name]
        show_legend = name not in names_in_legend
        fig.add_trace(
            go.Bar(
                x=filtered_data["coherenceID"],
                y=filtered_data["frequency"],
                name=name,
                marker=dict(color=color_mapping[name]),
                showlegend=show_legend
            ),
            row=2,
            col=1
        )
        names_in_legend.add(name)

    # 4. Add Coherence Score Average Line Graph (right column)
    fig.add_trace(
        go.Scatter(
            x=score_coherence_df["coherenceID"],
            y=score_coherence_df["coherenceScore"],
            mode='lines',
            name="Average Coherence Score",
            line=dict(color="black", width=1)
        ),
        row=2,
        col=2
    )

    # 5. Add RepeatID bar chart (stacked, left column)
    for name in freq_repeat_df["name"].unique():
        filtered_data = freq_repeat_df[freq_repeat_df["name"] == name]
        show_legend = name not in names_in_legend
        fig.add_trace(
            go.Bar(
                x=filtered_data["repeatID"],
                y=filtered_data["frequency"],
                name=name,
                marker=dict(color=color_mapping[name]),
                showlegend=show_legend
            ),
            row=3,
            col=1
        )
        names_in_legend.add(name)

    # 6. Add Repeat Score Average Line Graph (grouped by name, right column)
    for name in score_repeat_df["name"].unique():
        filtered_data = score_repeat_df[score_repeat_df["name"] == name]
        show_legend = name not in names_in_legend
        fig.add_trace(
            go.Scatter(
                x=filtered_data["repeatID"],
                y=filtered_data["repeatScore"],
                mode='lines',
                name=f"{name} - Average Repeat Score",
                line=dict(width=1),
                marker=dict(color=color_mapping[name]),
                showlegend=show_legend
            ),
            row=3,
            col=2
        )

    # Update layout for better visualization
    fig.update_layout(
        height=900,  # Shorter overall height for the figure
        width=1200,  # Adjust width for better visualization
        barmode='stack',  # Stack bars for RepeatID plot
        template="plotly_white",
        legend_title="Names"
    )

    # Update x-axes for all subplots
    fig.update_xaxes(tickmode="linear", range=x_range, dtick=5, showticklabels=True)

    return fig
