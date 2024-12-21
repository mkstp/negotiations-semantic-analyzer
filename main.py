def analyzeTranscript(location='demo_transcript', topicString = " ", anonymizeFlag=False):
    import fathomPreprocessor
    import parameterizer

    topics = topicString.split(",")
    topics = [word.strip() for word in topics]

    # set flag to true to anonymize speakers, set to false to preserve names
    location = f"meetingTranscripts/{location}.txt"
    raw = fathomPreprocessor.prepFile(location, anonymizeFlag)
    data = parameterizer.parameterize(raw[0], raw[1], raw[2], topics) # raw[0], raw[1], raw[2] = speakers, timespans, transcripts

    return data

def outputJson(output, fileName = 'demo_output'):
    import json

    fileName = f"meetingTranscripts/{fileName}.json"

    with open(fileName, "w") as json_file:
        json.dump(output, json_file, indent=4)

location = 'negotiation_roleplay/d_marc_2_12-19-2024'
topicString = 'safety, materials, roof'

output = analyzeTranscript(location, topicString, False)
outputJson(output, location)