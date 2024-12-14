import json
import pandas as pd

def analyzeTranscript(location='demoContent/demo_transcript.txt', topicString = "", anonymizeFlag=False):
    import fathomPreprocessor
    import parameterizer

    topics = topicString.split(",")
    topics = [word.strip() for word in topics]

    # set flag to true to anonymize speakers, set to false to preserve names
    raw = fathomPreprocessor.prepFile(location, anonymizeFlag)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2], topics) # raw[0], raw[1], raw[2] = speakers, timespans, transcripts

    return data

def computeMetrics(df):
    # Calculating the metrics
    avgAirTime = df.groupby(['name', 'turn'])['airTime'].sum().groupby('name').mean()
    avgWPM = df.groupby('name')['wpm'].mean()
    avgResponse = df.groupby('name')['responseScore'].mean()
    avgCoherence = df.groupby('name')['coherenceScore'].mean()
    countQuestions = df.groupby(['name', 'qType'])['qType'].count()
    countNarrative = df.groupby(['name', 'nType'])['nType'].count()
    countEmotion = df.groupby(['name', 'emotion'])['emotion'].count()
    countTopic = df.groupby(['name', 'topic'])['topic'].count()
    
    # Initializing the dictionary
    result = {}
    
    # Looping through unique names
    for name in df['name'].unique():
        # Creating nested dictionary for each name
        result[name] = {
            'avgAirTime': avgAirTime.get(name, None),
            'avgWPM': avgWPM.get(name, None),
            'avgResponse': avgResponse.get(name, None),
            'avgCoherence': avgCoherence.get(name, None),
            'countQuestions': countQuestions.loc[name].to_dict() if name in countQuestions else {},
            'countNarrative': countNarrative.loc[name].to_dict() if name in countNarrative else {},
            'countEmotion': countEmotion.loc[name].to_dict() if name in countEmotion else {},
            'countTopic': countTopic.loc[name].to_dict() if name in countTopic else {},
        }
    
    return result

def outputJson(output, fileName = 'test.json'):

    with open(fileName, "w") as json_file:
        json.dump(output, json_file, indent=4)

def showReport(fileName = 'test.json'):
    import visualizer

    df = pd.read_json(fileName)
    metrics = computeMetrics(df)
    print(metrics)
    # Create and show plots
    visualizer.plotWPMAirTime(df)
    visualizer.plotCoherenceResponsiveness(df)
    visualizer.plot_response_and_coherence_frequency(df)
    visualizer.plotNarrativeEmotion(df)

location = 'demoContent/demo_transcript.txt'
fileName = 'demoContent/demo_parameterized.json'
topicString = "Software, Links, Recording"

# output = analyzeTranscript(location, topicString, False)
# outputJson(output, fileName)
showReport(fileName)