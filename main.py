import analyzer
import plotter

location = 'demoContent/demo_transcript.txt'
# set flag to true to anonymize speakers, set to false to preserve names
data = analyzer.filePrep(location, False)

speakers = data[0]
timespans = data[1]
transcripts = data[2]

speechRateDict = analyzer.speechRate(speakers, timespans, transcripts)
airTimeDict = analyzer.airTime(speakers, timespans)
sentimentDict = analyzer.feelRate(speakers, transcripts)
congruenceDict = analyzer.congruence(transcripts)

print(analyzer.univariate('Speech rate', speechRateDict))
print(analyzer.univariate('Air time', airTimeDict))
print(analyzer.univariate('Sentiment', sentimentDict))
print(analyzer.univariate('Congruence', congruenceDict))

plotter.plotSpeech(speechRateDict)
plotter.plotTime(airTimeDict)
plotter.plotFeeling(sentimentDict)
plotter.plotCongruence(congruenceDict)
