# CONVO ANALYZER

This project investigates how communication similarity influences negotiation outcomes, using time-stamped, speaker-identified transcripts to measure both procedural and semantic alignment. The goal is to develop interventions that enhance collaboration between negotiators.

The hypothesis is that negotiators who speak at similar speeds and for comparable durations achieve more collaborative outcomes. Conversely, significant disparities in speech rate or speaking time may lead to less favorable results.

Moreover, the project posits that similarity has a greater impact on negotiation success than adherence to objective communication benchmarks. For instance, it is more critical for negotiators to share similar speech rates than to both maintain a specific rate, and for their speaking turns to be similarly timed rather than falling within a predefined range.

## Temporal similarity measures:
 
- time spoken per person (in seconds)
- rate of speaking per person (in wpm)

## Emotional similarity measures:

- topic
- emotion (positive, neutral, negative)

Using topic modeling and sentiment analysis, this project compares negotiators' emotional expressions, hypothesizing that shared positivity around specific topics increases the likelihood of agreement. Conflict resolution research supports this, suggesting that de-escalating negative emotions involves acknowledging and aligning with them before reframing to positivity, fostering collaboration and resolution.

When managing negative emotion, my favorite analogy is firefighting: if someone directs emotional "fire" at you and you try to douse it immediately (e.g., saying "calm down" or "this isn’t a big deal"), the "fire" often spreads — manifesting as heightened anger or passive aggression. Instead, skilled firefighters establish a controlled burn, containing the fire and starving it of fuel. In emotional terms, this means acknowledging and validating the other person's feelings to contain and de-escalate their intensity.

Practically, this involves avoiding dismissive phrases like "relax" or "you're overreacting." Instead, empathetic statements like "I see why you feel this way" or "That sounds really frustrating" signal understanding and create space for constructive dialogue. Matching emotions almost never requires mirroring their intensity or becoming negative yourself. Emotional alignment can often be achieved through calm yet empathetic responses, reinforcing your intent to connect rather than escalate. Effective de-escalation requires flexibility. Not all situations or individuals respond to the same techniques, and overly validating negative emotions may inadvertently reinforce them. 

The software will indicate how emotions are distributed across various topics. By flagging negative emotion, we can design interventions to reframe them to positive interests. 

## Semantic similarity:

- narrative type (first, second, third, passive)
- responsiveness
- question type (open-ended or closed-ended)

Negotiations involve patterns of self-disclosure, questioning, and acknowledgment, with balanced proportions of these elements indicating healthy collaboration. A rule-based system labels narrative and question types, while responsiveness is assessed using a sentence similarity transformer model.

Collaborative outcomes are less likely if negotiations focus heavily on third-person statements (e.g., references to people not present). Balanced "I" and "you" statements are preferred, as an imbalance may signal one party dominating or withholding their position.

Responsiveness measures how closely a negotiator's statement relates to the previous one. High responsiveness indicates on-topic dialogue and acknowledgment, while low responsiveness suggests "talking past one another," common in arguments where positions conflict.

Questioning patterns can indicate 

## Lexical similarity:

- word choice patterns
- coherence
- repetitiveness


![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/airtime.png?raw=true)

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/speechrate.png?raw=true)



![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/sentiment.png?raw=true)


![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/congruence.png?raw=true)

