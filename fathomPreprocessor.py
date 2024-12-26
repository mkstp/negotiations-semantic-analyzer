#this module pre-processes transcript outputs (in txt format) from the Fathom video conferencing software
import re
import datetime
import time

#helper functions
def convertTime(timeList, totalTime):
    #convert string timestamps to total seconds elapsed
    tempList = []
    for t in timeList:
        x = time.strptime(t.strip(),'%M:%S')
        x = int(datetime.timedelta(minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
        tempList.append(x)

    #this is imperfect because total time might be zero if the regex does not match
    #marc will fix later ;)    
    tempList.append(totalTime)

    #convert total seconds elapsed to total seconds spoken on each turn
    outputList = []
    for i in range(1, len(tempList)):
        diff = tempList[i] - tempList[i - 1]
        if diff > 0:
            outputList.append(diff)
        else:
            outputList.append(1)

    return outputList

def processSpeakerNames(nameList, anonymizeFlag=True):
    outputList = nameList
    #anonymize speaker names
    if anonymizeFlag:
        for idx, speaker in enumerate(set(outputList)):
            outputList = [name.replace(speaker, "Speaker" + str(idx)) for name in outputList]
    else:
        for idx, speaker in enumerate(set(outputList)):
            outputList = [name.replace(speaker, speaker.strip('- \n')) for name in outputList]
    return outputList

def cleanText(transcriptionList):
    #clean up transcription values
    transcriptionList = [t.strip().replace('\n', ' ') for t in transcriptionList]

    #regx substitute 
    transcriptionList = [re.sub(r'\s{2,}', ' ', t) for t in transcriptionList]

    transcriptionList = [re.sub(r'(?: like )|(?: like, )', ' ', t) for t in transcriptionList]
    return transcriptionList

#main function
def prepFile(content, anonymizeFlag=True):
    # FILE PREP: retreive raw transcript and split into lists and clean up values 
    # file = open(dir)
    # content = file.read()

    #extract and convert the total time of the convo from minutes to seconds
    totalConvoTime = re.search(r'(?:VIEW RECORDING)\s-\s\d{1,}', content)
    if totalConvoTime:
        totalConvoTime = int(totalConvoTime.group().split(" ")[-1]) * 60
    else:
        totalConvoTime = 0

    #remove hyperlinks
    content = re.sub(r'[A-Z]+:.+=\d{1,}.\d{1,}', ' ', content)
    content = content[content.find("---"):]

    #regx split by '0:00' OR '- First Last (moniker)\n' 
    content = re.split(r'(\d{1,2}\:\d{2}\s?)|(\-+\s.+\D\n)', content)[1:]
    content = list(filter(None, content))

    #initialize basic info lists
    timestamps = []
    speakers = []
    transcripts = []

    #assign values to individual lists
    for idx, i in enumerate(content):
        [timestamps, speakers, transcripts][idx%3].append(i)

    #massage data
    timespans = convertTime(timestamps, totalConvoTime)
    speakers = processSpeakerNames(speakers, anonymizeFlag)
    transcripts = cleanText(transcripts)

    return [speakers, timespans, transcripts]