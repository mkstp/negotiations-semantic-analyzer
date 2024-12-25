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

## Accommodating = High Responsive & Low Coherence: Upper Left Quadrant Analysis
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

## Discontinuous = Low Responsive & Low Coherence: Lower Left Quadrant Analysis

The lower left is for novel information which does not resemble anything spoken within the last few turns. This is where we would find a topic changer:

```
"turn": 3,
"name": "D C",
"previous": "B K",
"text": " Another question for me is always, what's the cost?",
"responseScore": 0.15,
"coherenceScore": 0.15,
```

Another kind of statement you can find in this quadrant is the implicit acknowledgement. This form of statement is only referential and not substantiated.

```
"turn": 2,
"name": "B K",
"previous": "D C",
"text": "Mm-hmm, I understand, I understand.",
"responseScore": 0.13,
"coherenceScore": 0.001,
```

The claim that B K understands lacks substantiation through semantic similarity. A negotiator who passively agrees, changes the topic, or asks unrelated questions discontinues the semantic line of conversation. Statements in this quadrant indicate a decision not to expand on their own or their partner's points. While such statements are valid and necessary in conversations, their overuse represents evasive tactics, and their effectiveness lies in balancing them with other types of statements.

## Directive = Low Responsive & High Coherence: Lower Right Quadrant Analysis

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

## Integrative = High Responsive & High Coherence: Upper Right Quadrant Analysis

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

## Distributed Differences in Responsiveness and Coherence Across Time

The following graph shows the distribution of the sum of scores for each statement colored by name. The negative values are the coherence levels by statement and the positive values are the levels of responses to those statements. The distribution differences reveal areas of alignment or divergence in what each negotiator prioritized within that turn.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/coh-res-rep.png?raw=true)

Coherence and responsiveness are imperfect mirrors of each other. For instance, in the ID range 10–25, the blue coherence bars reflect Y C's self-referential statements, while the red response bars show L S's selective responses. During this range, Y C's turn was highly coherent, with many statements interrelated and elaborative. In contrast, L S's responses highlight the selective importance placed on Y C's points. 

ID range(35-48) is a poignant example of undercoverage. We see a dip and sparsely populated section where Y C's turn statements become less coherent, and where L S is largely unresponsive.

By contrast, statement ID 14 has the highest coherence level for Y C:

```
"id": 14,
"turn": 6,
"name": "Y C",
"previous": "L S",
"text": " And I believe that if we have that resource, it's going to be a breakthrough improvement for the human history.",
```

But L S was completely unresponsive to that point. Y C then introduces some novel information by changing the subject:

```
"id": 19,
"turn": 6,
"name": "Y C",
"previous": "L S",
"text": " So, but the thing is that we will, we are currently competing with another company.",

...

"id": 22,
"turn": 6,
"name": "Y C",
"previous": "L S",
"text": " So if there's only one choice that you can make between us and the other company, I believe that will be a much better choice.",

"id": 23,
"turn": 6,
"name": "Y C",
"previous": "L S",
"text": " But I would also be curious about your concerns and your questions that you have, and then we'll try our best to answer them and make sure that we have the mutual understanding of the goal and then protect the environment as well.",
```

L S strongest responses are to ID 22 and 23 in Y C's turn:

```
"id": 25,
"turn": 7,
"name": "Leigh Sembaluk",
"previous": "Yichun Cheng",
"text": " One is we can make our decision on the other company and and see what goes, for us, the reason we have this algae is because we take care of the environment with it, it, you know, don't know if it existed elsewhere if it wasn't there, but you know, the fact that it exists where we are is because it's a very delicate balance, balance and we've taken care of it.",
"responseID": 22,
"responseScore": 0.51,

...

"id": 28,
"turn": 7,
"name": "L S",
"previous": "Y C",
"text": " The first thing that is non-negotiable for us is the algae if it's removed or moved off of our land, it will die and that our whole ecosystem suffers.",
"responseID": 23,
"responseScore": 0.41,

...

"id": 32,
"turn": 7,
"name": "L S",
"previous": "Y C",
"text": " So those are the couple main things and main concerns for us.",
"responseID": 23,
"responseScore": 0.43,

```

## Analysis of Accumulated Repetition 

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/repeat_scores.png?raw=true)

This chart represents out of turn repetitions of statements from earlier points in the conversation. A repetition is defined as the highest scoring similarity statement that is not in the present or previous turn. Strong repetitions indicate highly similar word choice and semantic alignment. An example:

```
"id": 10,
"turn": 6,
"name": "Y C",
"previous": "L S",
"text": "Yeah, I totally understand your concern, and then I respect how you really care for the environment.",

...

"id": 34,
"turn": 8,
"name": "Y C",
"previous": "L S",
"text": "I completely understand you, concern, you really care about the environment.",
"repID": 10,
"repScore": 0.91,
```

Repetition in negotiations often signals paraphrasing or summarizing, which acknowledges the other party's perspective. However, self-repetition can indicate a looping thought pattern or a sense of not being heard. Unaddressed important statements are more likely to be repeated, doubling the time spent conveying the same meaning. This additional time investment can emphasize a statement’s importance and invite coherence or responsiveness to clarify its meaning.

In the ID range 35–48, Y C's less self-referential statements, coupled with L S's lack of responsiveness, fostered an environment where repetition occurred, which can be interpreted as reducing the negotiation's overall efficiency.

### Conversational Modes

Conversational modes are points of focus within a discussion, appearing as peaks in a distribution. A highly left-skewed distribution with one mode early on suggests the conversation repeatedly circled initial points. In contrast, multiple modes indicate a discussion covering diverse topics rather than revisiting the same ones.







