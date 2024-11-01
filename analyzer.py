import re
import datetime
import time
from numpy import interp
import statistics

from transformers import pipeline
sentimentPipeline = pipeline("sentiment-analysis", 
model='nlptown/bert-base-multilingual-uncased-sentiment')

from sentence_transformers import SentenceTransformer
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

def convertTime(timeList, totalTime):
    #convert string timestamps to total seconds elapsed
    tempList = []
    for t in timeList:
        x = time.strptime(t.strip(),'%M:%S')
        tempList.append(int(datetime.timedelta(minutes=x.tm_min,seconds=x.tm_sec).total_seconds()))

    #this is imperfect because total time might be zero if the regex does not match
    #marc will fix later ;)    
    tempList.append(totalTime)

    #convert total seconds elapsed to total seconds spoken on each turn
    outputList = []
    for i in range(1, len(tempList)):
        outputList.append(tempList[i] - tempList[i - 1])

    return outputList

def anonymize(nameList):
    #anonymize speaker names
    outputList = nameList
    for idx, speaker in enumerate(set(outputList)):
        outputList = [name.replace(speaker, "Speaker" + str(idx)) for name in outputList]
    return outputList

def cleanText(transcriptionList):
    #clean up transcription values
    transcriptionList = [t.strip().replace('\n', ' ') for t in transcriptionList]
    #regx substitute 'ALLCAPSWORD: hyperlink timestamp' OR '    '
    transcriptionList = [re.sub(r'[A-Z]+:.+=\d{1,}.\d{1,}|\s{2,}', ' ', t) for t in transcriptionList]
    return transcriptionList

def speechRate(speakerList, timeList, transcriptList):
    #plotting how the speed of the conversation changed for each speaker

    #create list of speaking rates in wpm
    speakingRates = []
    for i in range(0, len(timeList)):
        wordLength = len(transcriptList[i].split(" "))
        speakingRates.append(int(wordLength/timeList[i] * 60))

    rateSpan = {}
    for i, r in zip(speakerList, speakingRates):
        if i in rateSpan:
            rateSpan[i].append(r)
        else:
            rateSpan[i] = [r]
    
    return rateSpan

def airTime(speakerList, timeList):
    #plotting how speakers took turns in the conversation
    air = {}
    for i, t in zip(speakerList, timeList):
        if i in air:
            air[i].append(t)
        else:
            air[i] = [t]

    return air

def feelRate(speakerList, transcriptList):
    #performs sentiment analysis on each transcript and 
    #organizes the scores according to the speaker

    sentimentList = []

    #the model used gives a score out of 5 then a confidence percentage
    #I took the score, then subtracted the tail of the confidence percentage
    #then mapped it between -1 and 1
    for text in transcriptList:
        sentiment = sentimentPipeline(text[:500])[0]
        score = round(int(sentiment['label'][0]) - (1 - sentiment['score']), 1)
        score = interp(score, [1, 5], [-1, 1])
        sentimentList.append(round(score, 2))

    output = {}
    for i, t in zip(speakerList, sentimentList):
        if i in output:
            output[i].append(t)
        else:
            output[i] = [t]
    
    return output

def congruence(transcriptList):
    #performs sentence analysis on successive text blocks to gauge how congruent
    #are the arguments made as they are spoken in turn
    #non congruence can signify a change in subject, whereas high congruence can
    #signify agreement or staying on the same topic
    congruenceScoreList = []

    for i in range(1, len(transcriptList)):
        sentences = [transcriptList[i][:500], transcriptList[i-1][:500]]
        embeddings = sentence_model.encode(sentences)
        similarities = sentence_model.similarity(embeddings, embeddings)
        congruenceScoreList.append(round(float(similarities[0][1]), 2))

    #turning it into a dictionary so it's formatted the same as everything else
    congruenceScoreDict = {'Speakers': congruenceScoreList}

    return congruenceScoreDict

def filePrep(dir):

    # FILE PREP: retreive raw transcript and split into lists and clean up values 
    file = open(dir)
    content = file.read()
    #extract and convert the total time of the convo from minutes to seconds
    totalConvoTime = re.search(r'(?:VIEW RECORDING)\s-\s\d{1,}', content)
    if totalConvoTime:
        totalConvoTime = int(totalConvoTime.group().split(" ")[-1]) * 60
    else:
        totalConvoTime = 0
    content = content[content.find("---"):]
    #regx split by '0:00' OR '- First Last (moniker)\n' 
    content = re.split(r'[\s](\d{1,2}\:\d{2}\s?)|(\-\s\w+\s\w+\s\(.+\)\n)', content)[1:]
    content = list(filter(None, content))
    timestamps = []
    speakers = []
    transcripts = []

    #assign values to individual lists
    for idx, i in enumerate(content):
        [timestamps, speakers, transcripts][idx%3].append(i)


    timespans = convertTime(timestamps, totalConvoTime)
    speakers = anonymize(speakers)
    transcripts = cleanText(transcripts)

    return [speakers, timespans, transcripts]

def univariate(name, d):
    #takes in a string for the name and a dictionary of speakers and their corresponding 
    #lists and outputs the mean and stdev for each parameter for each speaker
    output = []
    for key in d.keys():
        output.append(name + ' mean for ' + key + ' is: ' + str(round(sum(d[key])/len(d[key]), 1)))
        output.append(name + ' stdev for ' + key + ' is: ' + str(round(statistics.stdev(d[key]), 1)))
    return output