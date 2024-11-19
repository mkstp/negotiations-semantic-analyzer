# CONVO ANALYZER

Interpersonal relations which are characterized by a high degree of similarity generally lead to better negotiated outcomes for both parties. This project takes a time-stamped speaker identified transcript as input and measures similarity along the following parameters, plotted over rounds and turns taken:

- sentiment 
- sentence similarity 
- time spoken per person
- rate of speaking per person

A round is a sequence of two turns between two speakers, completed after the second speaker finishes.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/airtime.png?raw=true)

Airtime is measured as the timespan of one speaker's turn (in seconds)

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/speechrate.png?raw=true)

Rate of speech is calculated from the timespan (in seconds) of one speaker's turn divided by the number of words spoken, then multiplied by 60 to get words per minute.

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/sentiment.png?raw=true)

Sentiment takes the transcript of one speaker's turn and runs it through the 'nlptown/bert-base-multilingual-uncased-sentiment' NLP model (untuned) from Huggingface. This model was originally built from product review data to infer scores out of 5. The score for each speaker turn transcript is remapped to between -1 and 1 to demonstrate affective orientation. 

![alt text](https://github.com/mkstp/convo-analyzer/blob/main/demoContent/congruence.png?raw=true)

Congruence uses the 'all-MiniLM-L6-v2' NLP model (untuned) from Hugginface to compare one speaker's turn transcript to the next speaker's response. If the next speaker's response stays on topic, the congruence value will be high. However, when the topic is changed or not addressed in the response, the congruence value will spike lower. A consistently low congruence might signal a conversation that is adversarial in nature, where the speakers are arguing separate mandates without acknowledging the arguments of the other side. Alternatively, consistenly high congruence can signal a conversation that centers on only one topic where there is general agreement.

My intuition predicts that a 'healthy' conversation will proceed with some negative spikes in congruence (for topic changes), interlaced with ascending congruence values as speaker's move toward agreement on each individual topic. This will look like an ascending sawtooth waveform on the graph. 
