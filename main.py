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

def outputJson(output, fileName = 'test.json'):

    with open(fileName, "w") as json_file:
        json.dump(output, json_file, indent=4)

def showReport(fileName = 'test.json', filter=None):
    import analyzer
    import visualizer

    df = pd.read_json(fileName)

    metrics = analyzer.computeMetrics(df)
    print(analyzer.responseCoverage(df))
    print(metrics)

    # Create and show plots

    visualizer.plotWPMAirTime(df, filter)
    visualizer.plotCoherenceResponsiveness(df, filter)
    visualizer.plot_response_and_coherence_frequency(df, filter)
    visualizer.plotNarrativeEmotion(df, filter)
    # visualizer.generate_scatter_plot(df, filter)

location = 'demoContent/demo_transcript.txt'
fileName = 'demoContent/demo_parameterized.json'
topicString = "Software, Links, Recording"

output = analyzeTranscript(location, topicString, False)
outputJson(output, fileName)
showReport(fileName)