#this module contains the functions for detecting the parameters for analysis in a given transcript
import re
import zlib
import spacy
from transformers import pipeline
sentimentPipeline = pipeline("sentiment-analysis", model='cardiffnlp/twitter-roberta-base-sentiment-latest')

from sentence_transformers import SentenceTransformer, util
sentencePipeline = SentenceTransformer("all-MiniLM-L6-v2")

#helper functions
def speechRateDetector(timeList, transcriptList):
    #plotting how the speed of the conversation changed for each relationship  

    #create list of speaking rates in wpm
    speakingRates = []

    for i in range(0, len(timeList)):
        wordLength = len(transcriptList[i].split(" "))
        x = int(wordLength/timeList[i] * 60)
        if x < 400:
            speakingRates.append(x)
        else:
            speakingRates.append(150)
    
    return speakingRates

def narrativeDetector(sentence):
    #this function takes in a list of sentences and codes them according to their main narrative pronoun use
    output = ""

    #split the sentences into words, then filter them through the narrative lists
    sentence = sentence.lower()
    sentence = re.sub(r'(?:you know)|(?:i\'m like)', '', sentence) #removing a few stop words
    words = re.split(r'(\s|\'|\,)', sentence)
    wordSet = set(words)

    #this configuration prioritizes third person pronoun detection followed by second, first, then passive (no pronoun)
    #because I'm more interested to know when people are talking about other people behind their backs
    if len(wordSet.intersection({'he', 'him', 'his', 'she', 'her', 'hers', 'they', 'them', 'their', "theirs", "themself", "themselves", "herself", "himself"})) > 0:
        output = "third"

    elif len(wordSet.intersection({"you", "your", "yours", "yourself", "yourselves"})) > 0:
        output = "second"

    elif len(wordSet.intersection({'i', "me", "my", "we", "our", "mine", "ours", "us", "myself", "ourselves"})) > 0:
        output = "first"

    else:
        if len(sentence) > 1:
            output = "passive"

    return output

def questionDetector(sentence):
    #detects whether a question is open ended or not
    output = ""

    if "?" in sentence:
        sentence = sentence.lower()
        words = re.split(r'(\s|\')', sentence)
        wordSet = set(words)
        if len(wordSet.intersection({"why", "how", "what"})) > 0:
            output = "openEnded"
        else:
            output = "closedEnded"
    else:
        output = None #not a question

    return output

def affectDetector(sentence):
    #compute the sentiment score of each sentence
    sentiment = sentimentPipeline(sentence)[0]

    return (sentiment['label'], sentiment['score'])

def summaryGenerator(sentence):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(
        sentence, 
        max_length=100, 
        min_length=80, 
        do_sample=False)
    
    return summary[0]['summary_text']

def redundancyDetector(sentence):
    #calculates the amount of redundancy in a given sentence
    originalSize = len(sentence.encode('utf-8'))
    compressedSize = len(zlib.compress(sentence.encode('utf-8')))
    ratio = min(compressedSize / originalSize, 1)

    return ratio

def sentenceTagger(sentence):
    nlp = spacy.load("en_core_web_sm")
    data = nlp(sentence)
    posTags = [(token.text, token.pos_, spacy.explain(token.pos_)) for token in data]

    return posTags

def similarityDetector(sentenceList):
    #enconde and run sentences through the nlp model
    embeddings = sentencePipeline.encode(sentenceList, batch_size=32)
    similarities = sentencePipeline.similarity(embeddings, embeddings)
    
    return similarities

def matchTopic(transcriptList, topicList):
    topicEmbeddings = sentencePipeline.encode(topicList, convert_to_tensor=True)
    transcriptEmbeddings = sentencePipeline.encode(transcriptList, batch_size=32, convert_to_tensor=True)

    results = []

    for embedding in transcriptEmbeddings:
        similarities = util.cos_sim(embedding, topicEmbeddings)
        maxIdx = similarities.argmax().item()
        score = similarities[0][maxIdx].item()

        results.append((topicList[maxIdx], score))

    return results

def responsivenessCoherenceDetector(output, similarityTensors):
# this function will break down for meetings with more than two people

    lastTurn, myLastTurnIDs, lastTurnIDs, thisTurnIDs,  = 0, [], [], []

    for i in output:
        if i['turn'] != lastTurn:
            lastTurn, myLastTurnIDs, lastTurnIDs, thisTurnIDs = i['turn'], lastTurnIDs, thisTurnIDs, []

        # Calculate responseScores
        responseScores = [(id, float(similarityTensors[i['id']][id])) for id in lastTurnIDs]
        if responseScores:  # Ensure there are scores to evaluate
            maxResponsePair = max(responseScores, key=lambda x: x[1])  # Get (id, score) with max score
            i['responseID'], i['responseScore'] = maxResponsePair[0], maxResponsePair[1]
        else:
            i['responseID'], i['responseScore'] = None, None  # Handle cases with no scores

        # Calculate selfScores based on the speaker's turn IDs
        selfScores = [(id, float(similarityTensors[i['id']][id])) for id in (thisTurnIDs + myLastTurnIDs)]
        if selfScores:  # Ensure there are scores to evaluate
            maxSelfPair = max(selfScores, key=lambda x: x[1])  # Get (id, score) with max score
            i['coherenceID'], i['coherenceScore'] = maxSelfPair[0], maxSelfPair[1]
        else:
            i['coherenceID'], i['coherenceScore'] = None, None  # Handle cases with no scores

        repScores = [(id, float(similarityTensors[i['id']][id])) for id in range(i['id'] - 1, -1, -1)]
        if repScores: # Ensure there are scores to evaluate
            maxRepPair = max(repScores, key=lambda x: x[1])  # Get (id, score) with max score
            i['repID'], i['repScore'] = maxRepPair[0], maxRepPair[1]
        else:
            i['repID'], i['repScore'] = None, None  # Handle cases with no scores   

        thisTurnIDs.append(i['id'])

        # Calculate repetitions
        rep_scores = [
            id
            for id in range(i['id'] - 1, -1, -1)
            if float(similarityTensors[i['id']][id]) >= 0.6
        ]

        i['repetitions'] = rep_scores

    return output


#main function
def parameterize(speakerList, timeList, transcriptList, topicList):
    #speakerList: strings: names of each speaker
    #timeList: integers: timespan in seconds 
    #transcriptList: strings: what was said
    #all indices must align, so anyList[idx] must match the speaker to timespan to transcript
    output = []

    speechRates = speechRateDetector(timeList, transcriptList)

    #match topics to transcript list items
    topics = matchTopic(transcriptList, topicList) if topicList else [("N/A", 0) for i in transcriptList]

    #correlate filler word use


    sentenceList = []
    count = 0
    
    for idx1, speaker in enumerate(speakerList):

        delimiter= r'[.!?]|(?: But )'
        pattern = f'(.*?{delimiter})'
        transcript = re.findall(pattern, transcriptList[idx1])

        for sentence in transcript:
            time = int(len(sentence.split()) * 60 / speechRates[idx1])
            if time <= 1:
                continue
            sentenceList.append(sentence)
            emotion = affectDetector(sentence)
            compressionRatio = redundancyDetector(sentence)
            wordLength = len(sentence.split())

            data = {
                'id': count,
                'turn': idx1,
                'name': speaker,
                'previous': " " if idx1 == 0 else speakerList[idx1 - 1],
                'text': sentence,
                'airTime': time,
                'wpm': speechRates[idx1],
                # 'wordLength': wordLength, # unnecessary
                # 'efficiency': compressionRatio, #the implementation of this one does not make sense
                'qType': questionDetector(sentence),
                'nType': narrativeDetector(sentence),
                'topic': topics[idx1][0],
                'topicConfidence': topics[idx1][1],
                'emotion': emotion[0],
                'emotionConfidence': emotion[1]
            }
            count+=1
            output.append(data)

    similarities = similarityDetector(sentenceList)
    output = responsivenessCoherenceDetector(output, similarities)
    
    return output
