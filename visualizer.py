import matplotlib.pyplot as plt

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
    xaxis = [str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(1024/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 250)

    # add labels
    plt.xlabel("Rounds")
    plt.ylabel("Rate of Speech (wpm)")

    # plot multiple lines
    colours = ['red', 'blue', 'green']
    for idx, speaker in enumerate(dataDict.keys()):
        plt.plot(xaxis, dataDict[speaker], label= speaker, marker='', color= colours[idx%3], linewidth=2, alpha=1)
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
    xaxis = [str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(1024/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 300)

    # add labels
    plt.xlabel("Rounds")
    plt.ylabel("Air Time (s)")

    # plot multiple lines
    colours = ['red', 'blue', 'green']
    for idx, speaker in enumerate(dataDict.keys()):
        plt.plot(xaxis, dataDict[speaker], label= speaker, marker='', color= colours[idx%3], linewidth=2, alpha=1)
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
    xaxis = [str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(1024/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(-1, 1)

    # add labels
    plt.xlabel("Rounds")
    plt.ylabel("Sentiment")

    # plot multiple lines
    colours = ['red', 'blue', 'green']
    for idx, speaker in enumerate(dataDict.keys()):
        plt.plot(xaxis, dataDict[speaker], label= speaker, marker='', color= colours[idx%3], linewidth=2, alpha=1)
    plt.legend()

def plotCongruence(dataDict):
    #takes in a list of turn congruencies and plots it as a line graph

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
    xaxis = [str(i+1) for i in range(0, size)]

    # set figure size
    my_dpi=96
    plt.figure(figsize=(1024/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 1)

    # add labels
    plt.xlabel("Rounds")
    plt.ylabel("Congruence (perc)")

    # plot multiple lines
    colours = ['red', 'blue', 'green', 'black']
    for idx, speaker in enumerate(dataDict.keys()):
        plt.plot(xaxis, dataDict[speaker], label= speaker, marker='', color= colours[idx%len(colours)], linewidth=2, alpha=1)
    plt.legend()
