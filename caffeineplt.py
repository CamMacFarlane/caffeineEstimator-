import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime

artString = """
 ( (
    ) )
 ..........
 |        |]
  \      /    
   `----'
"""

caffeineInputString = """

How much caffeine did you have?
--------------------------------
You can enter the amount in mg,
'c' for a 12oz coffee
'C' for a 20oz coffee
't' for 12oz tea
'T' for 20oz tea..." 
---------------------------------

"""

days = 1
repeat = False
caf_add_times = []
caf_add_amounts = []


def inputTocaf(x):
    return{
        'c': 125,
        'C': 200,
        't': 30,
        'T': 60,
        "" : 125,
    }.get(x, x)

print(artString)

"""
Gets the following data from user:

caf_add_times
caf_add_amounts
repeat
days

"""
def collectData():
    global caf_add_times
    global caf_add_amounts
    global repeat
    global days

    while(True):
        usr_input = (input("What time did you have caffeine? \nIf you didn't have any (more) caffeine press enter\n"))
        if(usr_input == "done"):
            break
        elif(usr_input == ""):
            #if caf_add_times is empty fill it with default
            if not caf_add_times:
                caf_add_times.append(9)
                caf_add_amounts.append(125)
                return
            break
        
        caf_add_times.append(int(usr_input)+1)
        usr_input = input(caffeineInputString)

        caf_amount = int(inputTocaf(usr_input))

        caf_add_amounts.append(caf_amount)

    days = input("How many days would you like to plot? ")
    
    if days == "":
        days = 1
    else:
        days = int(days)

    if(days > 1):
        usr_input = input("Would you like to repeat your caffeine intake over all days? (y/n)")
        repeat = (usr_input == "y")

maxCaf = 0

def processData():
    global caf_add_times
    global caf_add_amounts
    global repeat
    global days
    global maxCaf
    hours = 24*days
    caf_pts = [0]*hours
    caf_pts[0] = 0
    

    for t in range(1, len(caf_pts)):
        if(repeat):
            if t % (24) in caf_add_times:
                caf_pts[t] = caf_add_amounts[caf_add_times.index(t % 24)]
        else:
            if t in caf_add_times:
                caf_pts[t] = caf_add_amounts[caf_add_times.index(t % 24)]

        caf_pts[t] += caf_pts[t-1]*np.power(0.5, 1/6)
    
        if caf_pts[t] > maxCaf:
            maxCaf = caf_pts[t]
    return caf_pts

def plotCaffine2(cafIntake):
    xl = [0]*24*days
    now = datetime.now()  
    for i in range(0, 24*days):
        xl[i] = datetime(now.year, now.month, day = (now.day + int(i/24)), hour = i%24  )

    data = [go.Scatter(
          x=xl,
          y=cafIntake)]
    py.plot(data)    
        
def plotCaffine(cafIntake):

    Y = np.array(cafIntake)
    X = np.array(list(range(0, 24*days)))
    fig, ax = plt.subplots()

    ax.plot(X, Y)

    ax.grid(True)
    plt.xlabel("Hours")
    plt.ylabel("Caffeine in body mg")
    plt.xticks(np.arange(min(X), max(X)+1, 2.0))

    ax.fill_between(X, 0, maxCaf + .25*maxCaf, where=((X % 24) < 7), facecolor='blue', alpha=0.5)
    ax.fill_between(X, 0, maxCaf + .25*maxCaf, where=(((X-1) % 24) > 20), facecolor='blue', alpha=0.5)

    ax.set_ylim([0, 1.25*maxCaf])
    plt.show()


collectData()
c = processData()
plotCaffine2(c)
