import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

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

def plotCoherenceResponsiveness(df, topic_filter=None):
    from sklearn.linear_model import LinearRegression

    # Optionally filter the DataFrame by topic
    if topic_filter:
        df = df[df['topic'] == topic_filter]

    # Group the data by name
    grouped = df.groupby('name')

    # Create a scatter plot
    fig = go.Figure()

    for name, group in grouped:

        # Drop NaN values for the regression analysis
        group = group.dropna(subset=['coherenceScore', 'responseScore'])

        # Add scatter points for each name
        fig.add_trace(go.Scatter(
            x=group['coherenceScore'],
            y=group['responseScore'],
            mode='markers',
            name=f'{name} - Points'
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
                name=f'{name} - Regression Line'
            ))

    # Update the layout for better visualization
    fig.update_layout(
        height=500,  # Adjust height to accommodate both graphs
        width=800,  # Adjust width for better visualization
        title=f"Scatter Plot with Linear Regression Lines{' for ' + topic_filter if topic_filter else ''}",
        xaxis_title="Coherence Score",
        yaxis_title="Responsiveness Score",
        legend_title="Names",
        template="plotly_white"
    )

    fig.show()

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

def plot_response_and_coherence_frequency(df, topic_filter=None):
    """
    Creates two frequency histograms:
    1. Frequency of ResponseIDs grouped by name.
    2. Frequency of CoherenceIDs grouped by name.

    Both histograms are displayed in a single figure with subplots.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
    """

    # Optionally filter the DataFrame by topic
    if topic_filter:
        df = df[df['topic'] == topic_filter]

    # Group by name and responseID, and count occurrences
    freq_response_df = df.groupby(["name", "responseID"]).size().reset_index(name="frequency")

    # Group by name and coherenceID, and count occurrences
    freq_coherence_df = df.groupby(["name", "coherenceID"]).size().reset_index(name="frequency")

    # Create a subplot figure
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(
        "Frequency of ResponseIDs by Name",
        "Frequency of CoherenceIDs by Name"
    ))

    # Add ResponseID bar chart
    for name in freq_response_df["name"].unique():
        filtered_data = freq_response_df[freq_response_df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["responseID"],
                y=filtered_data["frequency"],
                name=name,
                marker=dict(line=dict(width=0.8))
            ),
            row=1,
            col=1
        )

    # Add CoherenceID bar chart
    for name in freq_coherence_df["name"].unique():
        filtered_data = freq_coherence_df[freq_coherence_df["name"] == name]
        fig.add_trace(
            go.Bar(
                x=filtered_data["coherenceID"],
                y=filtered_data["frequency"],
                name=name,
                marker=dict(line=dict(width=0.8))
            ),
            row=2,
            col=1
        )

    # Update layout for better visualization
    fig.update_layout(
        height=800,  # Increase height to accommodate both graphs
        width=800,   # Adjust width for better visualization
        title_text="Frequency of ResponseIDs and CoherenceIDs by Name",
        xaxis=dict(
            tickmode="linear",
            dtick=5  # Set x-axis tick increment to 5
        ),
        xaxis2=dict(
            tickmode="linear",
            dtick=5  # Set x-axis tick increment to 5
        ),
        yaxis_title="Frequency",
        yaxis2_title="Frequency",
        legend_title="Names",
        template="plotly_white"
    )

    fig.show()
