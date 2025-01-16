"""
Marc St. Pierre 1/13/2025
This module contains the functions for detecting the parameters for analysis in a given transcript.
"""

import re
import spacy 

from transformers import pipeline
from scipy.signal import find_peaks
from sentence_transformers import SentenceTransformer, util

#Inittialize Pipelines
sentiment_pipeline = pipeline(
    "sentiment-analysis", model='cardiffnlp/twitter-roberta-base-sentiment-latest'
)
sentence_pipeline = SentenceTransformer("all-MiniLM-L6-v2")

#Helper Functions
def speech_rate_detector(time_list, transcript_list):
    """Calculate the speaking rate (words per minute) for each segment."""
    speaking_rates = []

    for i in range(len(time_list)):
        word_length = len(transcript_list[i].split(" "))
        rate = int(word_length / time_list[i] * 60)
        speaking_rates.append(rate if rate < 400 else 150)

    return speaking_rates


def narrative_detector(sentence):
    """Categorize sentences by the predominant narrative pronoun use."""
    sentence = sentence.lower()
    sentence = re.sub(r'(?:you know)|(?:i\'m like)', '', sentence)
    words = re.split(r'(\s|\'|,)', sentence)
    word_set = set(words)

    #this configuration prioritizes third person pronoun detection followed by second, first, then passive (no pronoun)
    #because I'm more interested to know when people are talking about other people 
    if word_set.intersection(
        {
            'he', 'him', 'his', 'she', 'her', 'hers', 'they', 'them', 'their', 'theirs',
            'themself', 'themselves', 'herself', 'himself'
        }
    ):
        return "third"

    if word_set.intersection(
        {"you", "your", "yours", "yourself", "yourselves"}
    ):
        return "second"

    if word_set.intersection(
        {'i', "me", "my", "we", "our", "mine", "ours", "us", "myself", "ourselves"}
    ):
        return "first"

    return "passive" if len(sentence) > 1 else ""


def question_detector(sentence):
    """Determine whether a question is open-ended or closed-ended."""
    if "?" in sentence:
        words = re.split(r'(\s|\')', sentence.lower())
        word_set = set(words)
        if word_set.intersection({"why", "how", "what"}):
            return "openEnded"
        return "closedEnded"

    return None


def affect_detector(sentence):
    """Compute the sentiment score of a sentence."""
    sentiment = sentiment_pipeline(sentence)[0]
    return sentiment['label'], sentiment['score']


def summary_generator(sentence):
    """Generate a summary using a pre-trained summarization model. does not work well for conversational data"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(
        sentence,
        max_length=100,
        min_length=80,
        do_sample=False
    )
    return summary[0]['summary_text']


def sentence_tagger(sentence):
    """Tag sentences with parts of speech."""
    nlp = spacy.load("en_core_web_sm")
    data = nlp(sentence)
    return [(token.text, token.pos_, spacy.explain(token.pos_)) for token in data]


def similarity_detector(sentence_list):
    """Calculate similarity scores between sentences."""
    embeddings = sentence_pipeline.encode(sentence_list, batch_size=32)
    return sentence_pipeline.similarity(embeddings, embeddings)


def match_topic(transcript_list, topic_list):
    """Match transcript sentences to the most similar topic from a given list."""
    topic_embeddings = sentence_pipeline.encode(topic_list, convert_to_tensor=True)
    transcript_embeddings = sentence_pipeline.encode(
        transcript_list, batch_size=32, convert_to_tensor=True
    )

    results = []
    for embedding in transcript_embeddings:
        similarities = util.cos_sim(embedding, topic_embeddings)
        max_idx = similarities.argmax().item()
        score = similarities[0][max_idx].item()
        results.append((topic_list[max_idx], score))

    return results


def responsiveness_coherence_detector(output, similarity_tensors):
    """Evaluate similarity between turn-takers and their own statements."""
    previous_turn = 0
    my_previous_turn_ids = []
    previous_turn_ids = []
    this_turn_ids = []

    for entry in output:
        if entry['turn'] != previous_turn:
            previous_turn = entry['turn']
            my_previous_turn_ids = previous_turn_ids
            previous_turn_ids = this_turn_ids
            this_turn_ids = []

        all_scores = similarity_tensors[entry['id']]

        if previous_turn_ids:
            # Calculate response scores
            response_scores = [
                (idx, float(all_scores[idx])) for idx in previous_turn_ids
            ]
            max_response_pair = max(response_scores, key=lambda x: x[1])
            entry['responseID'], entry['responseScore'] = max_response_pair
        else:
            entry['responseID'], entry['responseScore'] = None, None

        if (this_turn_ids + my_previous_turn_ids):
            # Calculate self scores
            self_scores = [
                (idx, float(all_scores[idx])) for idx in (this_turn_ids + my_previous_turn_ids)
            ]
            max_self_pair = max(self_scores, key=lambda x: x[1])
            entry['coherenceID'], entry['coherenceScore'] = max_self_pair
        else:
            entry['coherenceID'], entry['coherenceScore'] = None, None

        if entry['turn'] > 2:
            # Calculate repetition scores
            rep_scores = [
                (idx, float(all_scores[idx])) for idx in range(entry['id'] - len(this_turn_ids + previous_turn_ids + my_previous_turn_ids) - 1, -1, -1)
            ]
            max_rep_pair = max(rep_scores, key=lambda x: x[1])
            entry['repeatID'], entry['repeatScore'] = max_rep_pair
        else:
            entry['repeatID'], entry['repeatScore'] = None, None

        this_turn_ids.append(entry['id'])

        # Calculate local maximum distribution
        similarity_distribution = [
            float(all_scores[idx]) for idx in range(0, entry['id'] - 1)
        ]
        peaks, _ = find_peaks(similarity_distribution, height=0.1, prominence=0.3)
        entry['localMaxDistro'] = peaks.tolist()

    return output


# Main function
def parameterize(speaker_list, time_list, transcript_list):
    """Extract parameters for analysis from a transcript."""
    output = []
    speech_rates = speech_rate_detector(time_list, transcript_list)

    sentence_list = []
    count = 0

    for idx1, speaker in enumerate(speaker_list):
        delimiter = r'[.!?]|(?: But )'
        pattern = f'(.*?{delimiter})'
        transcript = re.findall(pattern, transcript_list[idx1])

        for sentence in transcript:
            time = int(len(sentence.split()) * 60 / speech_rates[idx1])
            if time <= 1:
                continue

            sentence_list.append(sentence)
            emotion = affect_detector(sentence)

            data = {
                'id': count,
                'turn': idx1,
                'name': speaker,
                'previous': " " if idx1 == 0 else speaker_list[idx1 - 1],
                'text': sentence,
                'airTime': time,
                'wpm': speech_rates[idx1],
                'qType': question_detector(sentence),
                'nType': narrative_detector(sentence),
                'topic': "test",
                'topicConfidence': 1.0,
                'emotion': emotion[0],
                'emotionConfidence': emotion[1],
            }
            count += 1
            output.append(data)

    similarities = similarity_detector(sentence_list)
    output = responsiveness_coherence_detector(output, similarities)

    return output
