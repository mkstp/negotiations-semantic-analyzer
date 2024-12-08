import fathomPreprocessor
import parameterizer
import visualizer
import json
import pandas as pd

location = 'demoContent/demo_transcript.txt'
fileName = 'test.json'
topicString = 'first topic, another topic'

location = 'meetingTranscripts/marek/11-06-24.txt'
fileName = 'marc_marek_11-06-24.json'
topicString = 'Relationships, Communication, Technology, Personal Development'

# location = 'meetingTranscripts/brady/11-28-2024.txt'
fileName = 'marc_brady_11-08-2024.json'
# topicString = 'Japan, Sea Animals, Food, Climate'

def outputJson(fileName = 'test.json', topicString = ""):

    topics = topicString.split(",")

    # set flag to true to anonymize speakers, set to false to preserve names
    raw = fathomPreprocessor.prepFile(location, anonymizeFlag=False)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2], topics)

    with open(fileName, "w") as json_file:
        json.dump(data, json_file, indent=4)

def showReport(fileName = 'test.json'):
    df = pd.read_json(fileName)

    # Create and show plots
    visualizer.plotResponsiveCoherence(df, 7)
    visualizer.plotScoresWithRegression(df)
    visualizer.plotEmotionTopic(df)

# outputJson(fileName, topicString)
showReport(fileName)