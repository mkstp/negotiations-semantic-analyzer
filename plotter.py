import matplotlib.pyplot as plt
import pandas as pd

def plotSpeech(dataDict):
    #takes in a dictionary of speakers and rates and plots them as line graphs
    # get the size of the largest list
    size = 0
    for key in dataDict.keys():
        compare = len(dataDict[key])
        if size == 0:
            size = compare
        elif size < compare:
            size = compare
        
    # equalize the smaller list to the larger
    for value in dataDict.values():
        while len(value) < size:
            value.append(None)

    # define domain
    xaxis = ["Round " + str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 300)

    # add labels
    plt.ylabel("Rate of Speech (wpm)")

    # plot multiple lines
    plt.plot(xaxis, dataDict['Speaker0'], label= 'Speaker0', marker='', color='red', linewidth=2, alpha=1)
    plt.plot(xaxis, dataDict['Speaker1'], label= 'Speaker1', marker='', color='blue', linewidth=2, alpha=1)
    plt.legend()

def plotTime(dataDict):
    #takes in a dictionary of talking times per speaker and plots them as line graphs
    # get the size of the largest list
    size = 0
    for key in dataDict.keys():
        compare = len(dataDict[key])
        if size == 0:
            size = compare
        elif size < compare:
            size = compare
        
    # equalize the smaller list to the larger
    for value in dataDict.values():
        while len(value) < size:
            value.append(None)

    # define domain
    xaxis = ["Round " + str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 200)

    # add labels
    plt.ylabel("Air Time (s)")

    # plot multiple lines
    plt.plot(xaxis, dataDict['Speaker0'], label= 'Speaker0', marker='', color='red', linewidth=2, alpha=1)
    plt.plot(xaxis, dataDict['Speaker1'], label= 'Speaker1', marker='', color='blue', linewidth=2, alpha=1)
    plt.legend()

def plotFeeling(dataDict):
    #takes in a dictionary of talking times per speaker and plots them as line graphs
    # get the size of the largest list
    size = 0
    for key in dataDict.keys():
        compare = len(dataDict[key])
        if size == 0:
            size = compare
        elif size < compare:
            size = compare
        
    # equalize the smaller list to the larger
    for value in dataDict.values():
        while len(value) < size:
            value.append(None)

    # define domain
    xaxis = ["Round " + str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(-1, 1)

    # add labels
    plt.ylabel("Sentiment")

    # plot multiple lines
    plt.plot(xaxis, dataDict['Speaker0'], label= 'Speaker0', marker='', color='red', linewidth=2, alpha=1)
    plt.plot(xaxis, dataDict['Speaker1'], label= 'Speaker1', marker='', color='blue', linewidth=2, alpha=1)
    plt.legend()

def plotCongruence(dataDict):
    #takes in a list of turn congruencies and plots it as a line graph

    # define domain
    size = len(dataDict['Speakers'])
    xaxis = ["Turn " + str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 1)

    # add labels
    plt.ylabel("Congruence (perc)")

    plt.plot(xaxis, dataDict['Speakers'], label='Speakers', marker='', color='black', linewidth=2, alpha=1)
    plt.legend()
