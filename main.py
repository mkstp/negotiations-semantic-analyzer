import fathomPreprocessor
import parameterizer
import statAnalyzer
import json

location = 'meetingTranscripts/marc_marek/11-06-24.txt'
# location = 'meetingTranscripts/datafeel1/datafeelnov1meeting.txt'
fileName = "test2.json"

def generateJson(location, fileName = 'test.json', anonymize = True, showSummary = False):

    # set flag to true to anonymize speakers, set to false to preserve names
    raw = fathomPreprocessor.prepFile(location, anonymize)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2])

    import json
    with open(fileName, "w") as json_file:
        json.dump(data, json_file, indent=4)

    if showSummary:
        metrics = statAnalyzer.computeMetrics(data)
        for i in metrics:
            print(i)


def defineTopics(location = 'test.json'):
    from collections import Counter
    with open(location, "r") as json_file:
        parameterOutput = json.load(json_file)

    similarities = [i['similarity'] for i in parameterOutput if 'similarity' in i]
    flattened = [ idx1 for idx2 in similarities for idx1 in idx2 ]
    words = [parameterOutput[id]['lemmas'].split() for id in flattened]
    flattened = [ idx1 for idx2 in words for idx1 in idx2 ]
    final = Counter(flattened).most_common()

    return final
    
    
# generateJson(location, fileName, False, False)
# print(defineTopics(fileName))