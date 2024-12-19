def analyzeTranscript(location='demoContent/demo_transcript', topicString = " ", anonymizeFlag=False):
    import fathomPreprocessor
    import parameterizer

    topics = topicString.split(",")
    topics = [word.strip() for word in topics]

    # set flag to true to anonymize speakers, set to false to preserve names
    location = f"meetingTranscripts/{location}.txt"
    raw = fathomPreprocessor.prepFile(location, anonymizeFlag)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2], topics) # raw[0], raw[1], raw[2] = speakers, timespans, transcripts

    return data

def outputJson(output, fileName = 'test'):
    import json

    fileName = f"meetingTranscripts/{fileName}.json"

    with open(fileName, "w") as json_file:
        json.dump(output, json_file, indent=4)

def showReport(fileName = 'test', filter=None):
    import analyzer
    import visualizer
    import pandas as pd

    fileName = f"meetingTranscripts/{fileName}.json"

    df = pd.read_json(fileName)

    metrics = analyzer.computeMetrics(df)
    print(metrics)

    # Create and show plots
    visualizer.plotWPMAirTime(df, filter)
    visualizer.plotNarrativeEmotion(df, filter)
    visualizer.plotCoherenceResponsiveness(df, filter)
    visualizer.analyze_cluster_proportions_with_distances(df, filter)
    visualizer.plot_response_and_coherence_frequency(df, filter)

location = 'negotiation_roleplay/d_b_12-10-2024'
topicString = 'algae, snails, elders, enzymes, economy, culture, Pfizer, alzheimer\'s, mother'

output = analyzeTranscript(location, topicString, True)
outputJson(output, location)
showReport(location)