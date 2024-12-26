import json
import pandas as pd

# calculates the proportion of responses of each person to the other person's statements
def responseCoverage(df):
    # Group statements by 'name' and count unique 'id's for each name
    statement_counts = df.groupby('previous')['id'].nunique()

    # Group responses by 'name' and count unique 'responseID's for each name
    response_counts = df.groupby('name')['responseID'].nunique()

    result = {}

    # Compute proportions of responses to their statements
    for name in statement_counts.index:  # Iterate over unique 'name's
        statement_count = statement_counts.get(name, 0)
        response_count = response_counts.get(name, 0)

        if statement_count == 0:  # Avoid division by zero
            result[name] = 0
        else:
            result[name] = response_count / statement_count  # Use floating-point division

    return result

# Calculating the metrics
def computeMetrics(df):
    avgAirTime = df.groupby(['name', 'turn'])['airTime'].sum().groupby('name').mean()
    avgWPM = df.groupby('name')['wpm'].mean()
    avgResponse = df.groupby('name')['responseScore'].mean()
    avgCoherence = df.groupby('name')['coherenceScore'].mean()
    countQuestions = df.groupby(['name', 'qType'])['qType'].count()
    countNarrative = df.groupby(['name', 'nType'])['nType'].count()
    countEmotion = df.groupby(['name', 'emotion'])['emotion'].count()
    countTopic = df.groupby(['name', 'topic'])['topic'].count()
    propCoverage = responseCoverage(df)
    
    # Initializing the dictionary
    result = {}
    
    # Looping through unique names
    for name in df['name'].unique():
        # Creating nested dictionary for each name
        result[name] = {
            'avgAirTime': avgAirTime.get(name, None),
            'avgWPM': avgWPM.get(name, None),
            'propResponseCover': propCoverage.get(name, None),
            'avgResponseScore': avgResponse.get(name, None),
            'avgCoherenceScore': avgCoherence.get(name, None),
            'countQuestions': countQuestions.loc[name].to_dict() if name in countQuestions else {},
            'countNarrative': countNarrative.loc[name].to_dict() if name in countNarrative else {},
            'countEmotion': countEmotion.loc[name].to_dict() if name in countEmotion else {},
            'countTopic': countTopic.loc[name].to_dict() if name in countTopic else {},
        }
    
    return result

def analyzeTranscript(content, fileName):
    import fathomPreprocessor
    import parameterizer

    raw = fathomPreprocessor.prepFile(content, False)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2]) # raw[0], raw[1], raw[2] = speakers, timespans, transcripts

    #save the new json file in the same location
    fileName = fileName[:-3] + "json"

    with open(fileName, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return pd.read_json(fileName)