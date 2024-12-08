import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

def plotResponsiveCoherence(df, windowLength):

    smoothCoherence = savgol_filter(df['coherenceScore'], window_length=windowLength, polyorder=2)

    smoothResponse = savgol_filter(df['responseScore'], window_length=windowLength, polyorder=2)


    fig1 = px.line(df, x="id", y=smoothCoherence, title='Coherence', color='name')
    fig2 = px.line(df, x="id", y=smoothResponse, title='Responsiveness', color='name')

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

def plotScoresWithRegression(df):

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
        title="Scatter Plot with Linear Regression Lines",
        xaxis_title="Coherence Score",
        yaxis_title="Responsiveness Score",
        legend_title="Names",
        template="plotly_white"
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