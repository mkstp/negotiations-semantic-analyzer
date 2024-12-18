# CONVO ANALYZER

working paper title: "Echoes and Omissions: A Semantic Similarity Analysis of Coherence, Responsiveness, and Repetition in Negotiation Dynamics"

This project investigates how communication similarity influences negotiation outcomes, using time-stamped, speaker-identified transcripts to measure both procedural and semantic alignment. The goal is to develop interventions that enhance collaboration between negotiators.

The hypothesis is that negotiators who speak at similar speeds and for comparable durations achieve more collaborative outcomes. Conversely, significant disparities in speech rate or speaking time may lead to less favorable results.

Moreover, the project posits that similarity has a greater impact on negotiation success than adherence to objective communication benchmarks. For instance, it is more critical for negotiators to share similar speech rates than to both maintain a specific rate, and for their speaking turns to be similarly timed rather than falling within a predefined range.

Given a transcript and list of topics, the scripts generate a json file with each formatted object:

```
"sentenceID": 16,
"turn": 7,
"name": "Speaker B",
"previous": "Speaker A",
"text": "I mean, that's basically what I got from her a lot, right?",
"airTime": 4,
"wpm": 169,
"wordLength": 12,
"qType": "closedEnded",
"nType": "third",
"topic": " Communication",
"topicConfidence": 0.1834290325641632,
"emotion": "neutral",
"emotionConfidence": 0.7459942102432251,
"responsivenessID": 13,
"responsivenessScore": 0.20540665090084076,
"coherenceID": 11,
"coherenceScore": 0.23469233512878418,
"repetitionID": [2, 7]
```

The json file is divided into individual sentences, where each turn represents a block of sentences where one speaker speaks. 

## Temporal similarity measures:
 
- time spoken per person (in seconds)
- rate of speaking per person (in wpm)

## Semantic similarity:

- question type (open-ended or closed-ended)
- narrative type (first, second, third, passive)

Negotiations involve patterns of self-disclosure, questioning, and acknowledgment, with balanced proportions of these elements indicating healthy collaboration. A rule-based system labels narrative and question types.

Collaborative outcomes are less likely if negotiations focus heavily on third-person statements (e.g., references to people not present). Balanced "I" and "you" statements are preferred, as an imbalance may signal one party dominating or withholding their position.

Questioning patterns can indicate 

## Emotional similarity measures:

- topic
- emotion (positive, neutral, negative)

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/emotionplot.png?raw=true)

Using topic modeling and sentiment analysis, this project compares negotiators' emotional expressions, hypothesizing that shared positivity around specific topics increases the likelihood of agreement. Conflict resolution research supports this, suggesting that de-escalating negative emotions involves acknowledging and aligning with them before reframing to positivity, fostering collaboration and resolution.

When managing negative emotion, my favorite analogy is firefighting: if someone directs emotional "fire" at you and you try to douse it immediately (e.g., saying "calm down" or "this isn’t a big deal"), the "fire" often spreads — manifesting as heightened anger or passive aggression. Instead, skilled firefighters establish a controlled burn, containing the fire and starving it of fuel. In emotional terms, this means acknowledging and validating the other person's feelings to contain and de-escalate their intensity.

Practically, this involves avoiding dismissive phrases like "relax" or "you're overreacting." Instead, empathetic statements like "I see why you feel this way" or "That sounds really frustrating" signal understanding and create space for constructive dialogue. Effective de-escalation requires flexibility. Not all situations or individuals respond to the same techniques, and care must be taken not to overly validate negative emotions which may inadvertently reinforce them. 

The software will indicate how emotions are distributed across various topics. By flagging negative emotion, we can design interventions to reframe them to positive interests. 

## Semantic similarity continued:

- responsiveness
- coherence
- repetitiveness

Responsiveness measures how closely a negotiator's statement relates to the previous negotiators turn. High responsiveness indicates on-topic dialogue and acknowledgment, while low responsiveness suggests "talking past one another," common in arguments where positions conflict.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/responsiveness_time.png?raw=true)

Coherence measures how closely a negotiator's statement relates to their own statements including from the previous turn. High coherence indicates the negotiator is following a strong semantic line of argument across turns.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/coherence_time.png?raw=true)

The idea is that in conversations where there is agreement, there will be both strong levels of coherence and strong levels of responsiveness from both negotiators relative to each other. I'm predicting that with these metrics, I will be able to identify points in the conversation where negotiators converge toward agreement, or diverge into conflict. 

### Relationships between Responsiveness and Coherence

High Responsiveness, High Coherence:
Occurs when one negotiator responds with clear semantic alignment to the other’s statements, fully exploring or building on their ideas. In extreme cases, this might involve repeating the other person’s points verbatim to emphasize understanding or foster connection.

High Responsiveness, Low Coherence:
Happens when responses address the most recent statement but lack continuity with earlier discussion. This can seem like abandoning a previous point to focus solely on the latest input.

Low Responsiveness, High Coherence:
Seen when a negotiator reiterates their earlier points, sometimes to clarify or emphasize them if they feel unheard. This can either reinforce arguments constructively or be used adversarially to ignore the other’s input.

Low Responsiveness, Low Coherence:
Occurs when the conversation abruptly shifts to an unrelated topic, either strategically or due to disorganization. It can reflect a breakdown in conversation flow or deliberate topic avoidance.

Each strategy can be used constructively or destructively, and effective negotiation often involves a mix of all these approaches.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/response_coherence_scatter.png?raw=true)

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/response_coherence_scatter_alt.png?raw=true)


Repetitiveness tracks the sentenceID's of any previous statement that is a 0.6 semantic similarity match to what is crrently being said. A skilled negotiator will be able to paraphrase and synthesize multiple aspects of what someone has said over time. This will be showon on the repetitiveness index as hits on sentence which are spoken by the other person distributed in strategic locations throughout the conversation. Alternatively, speakers which show a high hit rate of repetitions on their own sentences are repeating the same points, this could be because they have a underlying unresolved narrative loop in their minds which underpins the need to repeat themselves. 




## Lexical similarity:

- word choice patterns

I'm going to try and detect stylistic and disfluency patterns and compare them across negotiators, with the idea that if negotiators can mimic each other's speaking style they will increase their changes of a collaborative outcome. This is a cutting edge research area and there is at this time not a clear path for parametirizing speaking style where suggestions for transforming one negotiators speaking style to another's can be reliably made. 

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/cluster_analysis.png?raw=true)
![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/coh-res-rep.png?raw=true)



