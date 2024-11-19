#this module contains the functions for detecting the parameters for analysis in a given transcript
import re
import torch
import zlib
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
stopWords = set(stopwords.words('english'))
translator = str.maketrans('', '', string.punctuation)
lemmatizer = WordNetLemmatizer()

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
        output = "NaQ" #not a question

    return output

def affectDetector(sentenceList):
    #builds an output list of sentiment labels and scores for each sentence given
    output = []  
    
    from transformers import pipeline
    sentimentPipeline = pipeline("sentiment-analysis", model='cardiffnlp/twitter-roberta-base-sentiment-latest') 

    for sentence in sentenceList:
            #compute the sentiment score of each sentence
            sentiment = sentimentPipeline(sentence)[0]
            output.append((sentiment['label'], sentiment['score']))

    return output

def similarityDetector(sentenceList):
    
    from sentence_transformers import SentenceTransformer
    sentencePipeline = SentenceTransformer("all-MiniLM-L6-v2")

    #enconde and run sentences through the nlp model
    embeddings = sentencePipeline.encode(sentenceList, batch_size=25)
    similarities = sentencePipeline.similarity(embeddings, embeddings)
    
    return similarities

def maskFilter(tensor, matchThreshold=0.45):
    #inputs a tensor and filters according to a threshold, then returns a list of indices
    #where the filter was achieved
    simScores = tensor 
    mask = (simScores > matchThreshold) & (simScores < 0.99)
    filtered = torch.nonzero(mask, as_tuple=True)[0]

    return filtered.tolist()

def redundancyDetector(sentence):
    #calculates the amount of redundancy in a given sentence
    originalSize = len(sentence.encode('utf-8'))
    compressedSize = len(zlib.compress(sentence.encode('utf-8')))
    ratio = originalSize / compressedSize

    return ratio

def processSentence(sentence):
    sentence = sentence.lower()
    sentence = sentence.translate(translator)

    words = sentence.split()
    wordsFiltered = [lemmatizer.lemmatize(w) for w in words if w not in stopWords]

    return " ".join(wordsFiltered)

#main function
def parameterize(speakerList, timeList, transcriptList):
    #speakerList: strings: names of each speaker
    #timeList: integers: timespan in seconds 
    #transcriptList: strings: what was said
    #all indices must align, so anyList[idx] must match the speaker to timespan to transcript
    output = []

    speechRates = speechRateDetector(timeList, transcriptList)
    sentenceList = []
    count = 0

    for idx1, speaker in enumerate(speakerList):
        name = speaker
        turn = idx1
        previous = " " if idx1 == 0 else speakerList[idx1 - 1]
        rate = speechRates[idx1]
        rValue = redundancyDetector(transcriptList[idx1])

        delimiter= r'[.!?]|(?: But )'
        pattern = f'(.*?{delimiter})'
        transcript = re.findall(pattern, transcriptList[idx1])

        for sentence in transcript:
            time = int(len(sentence.split()) * 60 / rate)
            if time <= 1:
                continue
            sentenceList.append(sentence)
            rawSentence = sentence
            processedSentence= processSentence(sentence)
            qType = questionDetector(sentence)
            nType = narrativeDetector(sentence)

            data = {
                'id': count,
                'name': name,
                'turn': turn,
                'turnRedundancy': rValue,
                'previous': previous,
                'text': rawSentence,
                'lemmas': processedSentence,
                'wordLength': len(rawSentence),
                'airTime': time,
                'wpm': rate,
                'qType': qType,
                'nType': nType,
            }
            count+=1
            output.append(data)

    emotions = affectDetector(sentenceList)
    similarities = similarityDetector(sentenceList) 

    for idx3 in range(0, len(output)):
        output[idx3]['emotion'] = emotions[idx3][0]
        output[idx3]['emotionConfidence'] = emotions[idx3][1]
        output[idx3]['similarity'] = maskFilter(similarities[idx3])

    return output



