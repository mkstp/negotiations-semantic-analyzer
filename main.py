import analyzer
import plotter

location = 'content/demo_transcript.txt'
data = analyzer.filePrep(location)

speakers = data[0]
timespans = data[1]
transcripts = data[2]

speechRateDict = analyzer.speechRate(speakers, timespans, transcripts)
airTimeDict = analyzer.airTime(speakers, timespans)
sentimentDict = analyzer.feelRate(speakers, transcripts)
congruenceDict = analyzer.congruence(transcripts)

print(analyzer.univariate('Speech rate', speechRateDict))
print(analyzer.univariate('Air time', airTimeDict))
print(analyzer.univariate('Sentimate', sentimentDict))
print(analyzer.univariate('Congruence', congruenceDict))

plotter.plotSpeech(speechRateDict)
plotter.plotTime(airTimeDict)
plotter.plotFeeling(sentimentDict)
plotter.plotCongruence(congruenceDict)
