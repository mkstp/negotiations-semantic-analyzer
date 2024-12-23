# Echoes and Omissions: A Semantic Similarity Analysis of Coherence, Responsiveness, and Repetition in Negotiation Dynamics

This project investigates how communication similarity influences negotiation outcomes, using time-stamped, speaker-identified transcripts to measure both procedural and semantic alignment. The goal is to understand conversational speech through the lens of similarity to develop interventions that enhance collaboration between negotiators.

The hypothesis is that negotiators who speak similarly achieve more collaborative outcomes. Conversely, significant disparities in how speech is used may lead to less favorable results.

Given a transcript, the application generates a json file with formatted objects:

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

The json objects log data on individual sentences, where each turn represents a block of sentences where one speaker speaks. 

## Temporal similarity
 
- airTime = time spoken per person (in seconds)
- wpm = words per minutes; the rate of speaking per person per turn

## Categorical similarity

- question type (open-ended or closed-ended)
- narrative type (first, second, third, passive)
- topic (matches from a given topic list)
- emotion (positive, neutral, negative)

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/emotionplot.png?raw=true)

Negotiations involve patterns of self-disclosure, questioning, and acknowledgment, with balanced proportions of these elements indicating healthy collaboration. A rule-based system labels narrative and question types.

Collaborative outcomes are less likely if negotiations focus heavily on third-person statements (e.g., references to people not present). Balanced "I" and "you" statements are preferred, as an imbalance may signal one party dominating or withholding their position.

Using sentiment analysis, this compares negotiators' emotional expressions, hypothesizing that shared positivity around specific topics increases the likelihood of agreement. Conflict resolution research supports this, suggesting that de-escalating negative emotions involves acknowledging and aligning with them before reframing to positivity, fostering collaboration and resolution.

The software will indicate how emotions are distributed across various topics. By flagging negative emotion, we can design interventions to reframe them to positive interests. 

# Measuring Semantic Similarity: Description of Roleplay Experiment

6 volunteers participated in a 20minute negotiation roleplay in a virtual setting. Participants were randomly paired, then separated into parties and each given negotiation mandates.  

Party 1's Core Mandate Objective: secure access from a local fishing village to harvest a rare algae for research to cure Alzheimer's 

Party 2's Core Mandate Objective: prevent the imminent collapse of the village’s fishing economy, where any depletion of fundamental food sources will cost the livelihoods and health of the village's population.

This roleplay exercise is a form of ‘orange problem’, where both sides have mandates that are seemingly incompatible. But through interest based negotiation, both sides can achieve 100% of their mandates provided they establish trust and share all relevant information. 

## Analysis of Semantic Similarity Results

- responsiveness
- coherence
- repetitiveness

Coherence measures how self-similar a negotiator's statements are within their turn and compared to their previous turn, calculated as the maximum cosine similarity between statements from the current and previous turns.

Responsiveness measures how similar a negotiator’s statements are to their partner’s previous statements, based on the maximum cosine similarity. Both metrics are derived using a transformer model (ai) to embed semantic meaning into vector space and calculate distances between vectors. 

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/response_coherence_scatter.png?raw=true)

This analysis compares linear regression lines plotting 'coherence' against 'responsiveness' for each negotiator. Each dot represents a single statement (one sentence) made by a negotiator. 

The following overview examines the proportion of statements within each quadrant of the graph.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/cluster_analysis.png?raw=true)

## Accommodating = High Responsive / Low Coherence: Upper Left Quadrant Analysis
If we divide the graph into quadrants, the upper left portion of the graph represents statements that are very responsive to what the last negotiator has said, but have little to do with what the current negotiator is trying to say. Example:

```
"turn": 2,
"name": "B K",
"previous": "D C",
"text": " And then if there is a medicine that can totally cure Alzheimer's disease, what do you think about that?",

"turn": 3,
"name": "D C",
"previous": "B K",
"text": " Another question for me is always, what's the cost?",

"turn": 4,
"name": "B K",
"previous": "D C",
"text": "What would be the cost that you are concerned about or you will be interested in knowing?",
"responseScore": 0.61,
"coherenceScore": 0.09,
```

In this example, D C has started to address cost during turn 3, and then on the next turn, B K has asked an open-ended probing question which directly addresses this. But this question had little similarity with B K's previous statements on Alzheimer’s.

## Discontinuous = Low Responsive / Low Coherence: Lower Left Quadrant Analysis

The lower left is for novel information which does not resemble anything spoken within the last few turns. This is where we would find a topic changer:

```
"turn": 3,
"name": "D C",
"previous": "B K",
"text": " Another question for me is always, what's the cost?",
"responseScore": 0.15,
"coherenceScore": 0.15,
```

Another kind of statement you can find in this quadrant is the passive acknowledgement. This form of statement is only referential and not substantiated.

```
"turn": 2,
"name": "B K",
"previous": "D C",
"text": "Mm-hmm, I understand, I understand.",
"responseScore": 0.13,
"coherenceScore": 0.001,
```

The claim that B K understands lacks substantiation through semantic similarity. A negotiator who passively agrees, changes the topic, or asks unrelated questions discontinues the semantic line of conversation. Statements in this quadrant indicate a decision not to expand on their own or their partner's points. While such statements are valid and necessary in conversations, their overuse represents evasive tactics, and their effectiveness lies in balancing them with other types of statements.

## Directive = Low Responsive / High Coherence: Lower Right Quadrant Analysis

This quadrant is for statements which are highly self-similar (in some cases exact repeats) but not responsive to the other person. These kinds of statements repeat or expand on something a negotiator is currently talking about.

```
"turn": 4,
"name": "B K",
"previous": "D C",
"text": "What would be the cost that you are concerned about or you will be interested in knowing?",

"turn": 5,
"name": "D C",
"previous": "B K",
"text": "Well, I mean, you know, being indigenous going back, it's more of the environment is the important thing, and we're stewards of that.",
"responseScore": 0.12,
"coherenceScore": 0.22,

"turn": 5,
"name": "D C",
"previous": "B K",
"text": " So, that's our responsibility is to make sure that we don't take priority over nature, over what sustains us.",
"responseScore": 0.08,
"coherenceScore": 0.58,
```

In this example, D C changes the topic (a discontinuity) and introduces some novel information which expands in the next statement. 

A negotiator who spends a lot of time in this quadrant will have a more independent approach to leading the conversation in a particular direction. This is further supported by D C's post roleplay survey results on the topic of environmental stewardship.

“I feel it went well in that I didn't move from the position of environment first and made that clear.  There was a clear responsibility to ensure that the ecosystem being upset means that the village loses out.”

## Integrative = High Responsive / High Coherence: Upper Right Quadrant Analysis

These kinds of statements are highly-self similar, even repetitive, and also highly responsive to what the other negotiator is saying. They are integrative in the sense that they tend to discuss the similarities the two negotiators have in common. 

```
"turn": 5,
"name": "D C",
"previous": "B K",
"text": "Well, I mean, you know, being indigenous going back, it's more of the environment is the important thing, and we're stewards of that.",

"turn": 6,
"name": "B K",
"previous": "D C",
"text": " And then I think exactly the same as you do, and I also really like the land, and I would to protect the environment that we all have together.",

"turn": 7,
"name": "D C",
"previous": "B K",
"text": " So that's one thing that has to stay because otherwise the whole ecosystem just falls apart and also I guess acknowledging that it's on our land so that everything that you come into it have to actually work in conjunction with us.",
"responseScore": 0.57,
"coherenceScore": 0.67,
```
In this negotiation, both agreed that protecting the environment was important. 


![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/response_coherence_scatter_alt.png?raw=true)


Repetitiveness tracks the sentenceID's of any previous statement that is a 0.6 semantic similarity match to what is crrently being said. A skilled negotiator will be able to paraphrase and synthesize multiple aspects of what someone has said over time. This will be showon on the repetitiveness index as hits on sentence which are spoken by the other person distributed in strategic locations throughout the conversation. Alternatively, speakers which show a high hit rate of repetitions on their own sentences are repeating the same points, this could be because they have a underlying unresolved narrative loop in their minds which underpins the need to repeat themselves. 




## Lexical similarity:

- word choice patterns

I'm going to try and detect stylistic and disfluency patterns and compare them across negotiators, with the idea that if negotiators can mimic each other's speaking style they will increase their changes of a collaborative outcome. This is a cutting edge research area and there is at this time not a clear path for parametirizing speaking style where suggestions for transforming one negotiators speaking style to another's can be reliably made. 

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/coh-res-rep.png?raw=true)



