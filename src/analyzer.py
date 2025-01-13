"""
Marc St. Pierre 1/13/2025
This module provides functionality to analyze conversation transcripts and compute 
various metrics. It also includes functionality to save processed 
transcripts as JSON files.
"""

import json
import pandas as pd

# Helper Functions
def response_coverage(df):
    """
    Calculate the proportion of responses for each person to other people's statements.

    Parameters:
    df (pd.DataFrame): DataFrame containing conversation data with 'previous', 'id',
                       'name', and 'responseID' columns.

    Returns:
    dict: A dictionary where the keys are names and the values are the proportion
          of responses made to other people's statements.
    """
    # Group statements by 'previous' and count unique 'id's for each name
    statement_counts = df.groupby('previous')['id'].nunique()

    # Group responses by 'name' and count unique 'responseID's for each name
    response_counts = df.groupby('name')['responseID'].nunique()

    result = {}

    # Compute proportions of responses to their statements
    for name in statement_counts.index:
        statement_count = statement_counts.get(name, 0)
        response_count = response_counts.get(name, 0)

        # Avoid division by zero
        result[name] = 0 if statement_count == 0 else response_count / statement_count

    return result


def compute_metrics(df):
    """
    Compute various metrics for each person in the conversation.

    Parameters:
    df (pd.DataFrame): DataFrame containing conversation data with columns such as
                       'name', 'airTime', 'turn', 'wpm', 'responseScore', 
                       'coherenceScore', 'qType', 'nType', 'emotion', and 'topic'.

    Returns:
    dict: A dictionary where each key is a person's name and the value is another
          dictionary containing various computed metrics.
    """
    avg_air_time = df.groupby(['name', 'turn'])['airTime'].sum().groupby('name').mean()
    avg_wpm = df.groupby('name')['wpm'].mean()
    avg_response = df.groupby('name')['responseScore'].mean()
    avg_coherence = df.groupby('name')['coherenceScore'].mean()
    count_questions = df.groupby(['name', 'qType'])['qType'].count()
    count_narrative = df.groupby(['name', 'nType'])['nType'].count()
    count_emotion = df.groupby(['name', 'emotion'])['emotion'].count()
    count_topic = df.groupby(['name', 'topic'])['topic'].count()
    prop_coverage = response_coverage(df)

    result = {}

    # Loop through unique names
    for name in df['name'].unique():
        result[name] = {
            'avgAirTime': avg_air_time.get(name, None),
            'avgWPM': avg_wpm.get(name, None),
            'propResponseCover': prop_coverage.get(name, None),
            'avgResponseScore': avg_response.get(name, None),
            'avgCoherenceScore': avg_coherence.get(name, None),
            'countQuestions': count_questions.loc[name].to_dict() if name in count_questions else {},
            'countNarrative': count_narrative.loc[name].to_dict() if name in count_narrative else {},
            'countEmotion': count_emotion.loc[name].to_dict() if name in count_emotion else {},
            'countTopic': count_topic.loc[name].to_dict() if name in count_topic else {},
        }

    return result


def analyze_transcript(content, file_name):
    """
    Analyze the transcript data, process it, and save the result as a JSON file.

    Parameters:
    content (str): Raw transcript content.
    file_name (str): The name of the file where the processed data will be saved.

    Returns:
    pd.DataFrame: A DataFrame loaded from the saved JSON file containing the processed data.
    """
    import fathom_preprocessor
    import parameterizer

    # Preprocess the file content
    raw = fathom_preprocessor.prep_file(content, False)

    # Parameterize the raw data (speakers, timespans, transcripts)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2])

    # Save the new JSON file in the same location
    file_name = file_name[:-3] + "json"

    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return pd.read_json(file_name)