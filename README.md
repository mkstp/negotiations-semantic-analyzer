
# Summary

This project investigates how communication similarity influences negotiation outcomes, using time-stamped, speaker-identified transcripts to measure semantic alignment. The goal is to understand conversational speech through the lens of similarity to develop interventions that enhance collaboration between negotiators.

A well studied phenemenon: negotiators who speak similarly achieve more collaborative outcomes. Conversely, disparities in speech lead to less favorable results. Is this true at the linguistic level of semantics?

## Example App Outputs:

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/res/cluster_analysis.png?raw=true)
![alt text](https://github.com/mkstp/convo-analyzer/blob/main/res/emotionplot.png?raw=true)

# How to:

1. Install necessary [requirements](/doc/requirements.txt)
2. Open terminal from the root folder and run *python src/app.py* 
3. This will open up a clickable link (host ip address) to a webpage
4. From the 'Drag and Drop' button at the top of the webpage, navigate them select "demo_transcript.json"
5. Wait a few seconds
6. Results of conversation should be visualized

## How to generate your own transcripts and json files

1. Sign up for the free meeting assistant software [Fathom](https://fathom.video/home)
2. Host a virtual meeting with one other person (currently only tested to work with transcripts up to 2 speakers)
3. Save a copy of the transcript as 'your_transcript.txt'

> [!NOTE]
> the app uses this [parser module](/src/fathom_preprocessor.py) to prep the file for parameterization. Best before date: 1/13/2025

4. Open terminal from the root folder and run *python src/app.py* 
4. Follow the link and use the 'Drag and Drop' button and select 'your_transcript.txt'
5. Wait between 15s to few minutes (this may take longer if your are downloading ai models for the first time)
6. 'your_transcript.json' will be saved in the same directory
7. Results of conversation should be visualized

# JSON Output Format and Description of Parameters

Given a fathom transcript, the [parameterizer module](/src/parameterizer.py) generates a json file with formatted objects:

```
"id": 35,
"turn": 8,
"name": "D C",
"previous": "B K",
"text": " We are very involved in the eco aspect of the entire operation.",
"airTime": 6,
"wpm": 113,
"qType": null,
"nType": "first",
"topic": "ecosystem",
"topicConfidence": 0.37485435605049133,
"emotion": "neutral",
"emotionConfidence": 0.5431026220321655,
"responseID": 30,
"responseScore": 0.26121166348457336,
"coherenceID": 25,
"coherenceScore": 0.22765521705150604,
"repeatID": 3,
"repeatScore": 0.4523921310901642,
"localMaxDistro": [
    20
]
```

The json objects log data on individual sentences, where each turn represents a block of sentence id's where one speaker speaks. 

## Temporal similarity
 
- airTime = time spoken per person (in seconds)
- wpm = words per minutes; the rate of speaking per person per turn

## Categorical similarity

- question type (open-ended or closed-ended)
- narrative type (first, second, third, passive)

Negotiations involve patterns of self-disclosure, questioning, and acknowledgment, with balanced proportions of these elements indicating healthy collaboration. A rule-based system labels narrative and question types.

Collaborative outcomes are less likely if negotiations focus heavily on third-person statements (e.g., references to people not present). Balanced "I" and "you" statements are preferred, as an imbalance may signal one party dominating or withholding their position.

## Semantic Similarity

- topic
- emotion (positive, neutral, negative)

Using sentiment analysis, this compares negotiators' emotional expressions, hypothesizing that shared positivity around specific topics increases the likelihood of agreement. Conflict resolution research supports this, suggesting that de-escalating negative emotions involves acknowledging and aligning with them before reframing to positivity, fostering collaboration and resolution.

The software will indicate how emotions are distributed across various topics. By flagging negative emotion, we can design interventions to reframe them to positive interests. 

- coherence
- responsiveness
- repetition

Coherence measures how self-similar a negotiator's statements are within their turn and compared to their previous turn, calculated as the maximum cosine similarity between statements from the current and previous turns.

Responsiveness measures how similar a negotiator’s statements are to their partner’s previous statements, based on the maximum cosine similarity. Both metrics are derived using a transformer model (ai) to embed semantic meaning into vector space and calculate distances between vectors.

A repetition is defined as the highest scoring similarity statement that is not in the present or previous turn. Strong repetitions indicate highly similar word choice and semantic alignment.

- localMaxDistro

This gives you the sentence indices of the relative peaks in the similarity distributions of all sentences from both speakers for all previous turns included the current one. 

# Interpreting Visuals

> [!NOTE]
> For an in depth analysis of how each graph is used in the context of a negotiation, please review the [experiment results](/doc/negotiation_results.md) file

> [!Note]
> A [bibliography](/doc/references.md) and [acknowledgements](/doc/acknowledgments.md) for this project are available in the documentation folder
