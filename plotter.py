import matplotlib.pyplot as plt
import pandas as pd

def plotSpeech(rates):
    #takes in a dictionary of speakers and rates and plots them as line graphs
    # equalize the length of each list for plotting
    size = 0
    for key in rates.keys():
        compare = len(rates[key])
        if size == 0:
            size = compare
        elif size > compare:
            size = compare

    # Make a data frame
    df=pd.DataFrame({
        'x': ["Round " + str(i+1) for i in range(0, size)], 
        'y1': rates['Speaker0'][:size], 
        'y2': rates['Speaker1'][:size]
        })

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 300)

    # add labels
    plt.ylabel("Rate of Speech (wpm)")

    # plot multiple lines
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color='black', linewidth=2, alpha=1)

def plotTime(times):
    #takes in a dictionary of talking times per speaker and plots them as line graphs
    # equalize the length of each list for plotting
    size = 0
    for key in times.keys():
        compare = len(times[key])
        if size == 0:
            size = compare
        elif size > compare:
            size = compare

    # Make a data frame
    df=pd.DataFrame({
        'x': ["Round " + str(i+1) for i in range(0, size)], 
        'y1': times['Speaker0'][:size], 
        'y2': times['Speaker1'][:size]
        })

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 200)

    # add labels
    plt.ylabel("Air Time (s)")

    # plot multiple lines
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color='black', linewidth=2, alpha=1)

def plotFeeling(sentiments):
    #takes in a dictionary of talking times per speaker and plots them as line graphs
    # equalize the length of each list for plotting
    size = 0
    for key in sentiments.keys():
        compare = len(sentiments[key])
        if size == 0:
            size = compare
        elif size > compare:
            size = compare

    # Make a data frame
    df=pd.DataFrame({
        'x': ["Round " + str(i+1) for i in range(0, size)], 
        'y1': sentiments['Speaker0'][:size], 
        'y2': sentiments['Speaker1'][:size]
        })

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(-1, 1)

    # add labels
    plt.ylabel("Sentimate")

    # plot multiple lines
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color='black', linewidth=2, alpha=1)

def plotCongruence(similarity):
    #takes in a list of turn congruencies and plots it as a line graph
    size = len(similarity['Speakers'])

    # Make a data frame
    df=pd.DataFrame({
        'x': ["Turn " + str(i+1) for i in range(0, size)], 
        'y1': similarity['Speakers'][:size] 
        })

    # set figure size
    my_dpi=96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

    # set range
    plt.ylim(0, 1)

    # add labels
    plt.ylabel("Congruence (perc)")

    # plot multiple lines
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color='black', linewidth=2, alpha=1)
