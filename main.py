import fathomPreprocessor
import parameterizer
import analyzer
import json

location = 'demoContent/demo_transcript.txt'
fileName = 'test.json'
topicString = 'first topic, another topic'
topics = topicString.split(",")


def outputJson(fileName = 'test.json', topicList = []):

    # set flag to true to anonymize speakers, set to false to preserve names
    raw = fathomPreprocessor.prepFile(location, anonymizeFlag=False)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2], topicList)

    with open(fileName, "w") as json_file:
        json.dump(data, json_file, indent=4)

outputJson(fileName, topics)

def runAnalysis(fileName = 'test.json'):
    with open(fileName, "r") as json_file:
        data = json.load(json_file)

    output = analyzer.computeMetrics(data)
    # analyzer.computeTopics(data)

    return output

# print(runAnalysis(fileName))