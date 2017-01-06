import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

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
    }.get(x, x)


# begin
print(artString)
while(True):
    usr_input = (input("What time did you have caffeine? \nIf you didn't have any (more) caffeine you can type 'done'\n"))
    if(usr_input == "done"):
        break
    caf_add_times.append(int(usr_input)+1)
    usr_input = input(caffeineInputString)

    caf_amount = int(inputTocaf(usr_input))

    caf_add_amounts.append(caf_amount)

days = int(input("How many days would you like to plot? "))

if(days > 1):
    usr_input = input("Would you like to repeat your caffeine intake over all days? (y/n)")
    repeat = (usr_input == "y")

hours = 24*days
caf_pts = [0]*hours
caf_pts[0] = 0
maxCaf = 0

for t in range(1, len(caf_pts)):
    if(repeat):
        if t % (24) in caf_add_times:
            caf_pts[t] = caf_add_amounts[caf_add_times.index(t % 24)]
    else:
        if t in caf_add_times:
            caf_pts[t] = caf_add_amounts[caf_add_times.index(t % 24)]

    caf_pts[t] += caf_pts[t-1]*np.power(0.5, 1/(6))
    
    if caf_pts[t] > maxCaf:
        maxCaf = caf_pts[t]

Y = np.array(caf_pts)
X = np.array(list(range(0, 24*days)))
fig, ax = plt.subplots()
ax.plot(X, Y)
ax.grid(True)
plt.xlabel("hours")
plt.ylabel("caffeine in body mg")
plt.xticks(np.arange(min(X), max(X)+1, 1.0))


ax.fill_between(X, 0, maxCaf + .25*maxCaf, where=((X % 24) < 7), facecolor='red', alpha=0.5)
ax.fill_between(X, 0, maxCaf + .25*maxCaf, where=(((X-1) % 24) > 20), facecolor='red', alpha=0.5)

ax.set_ylim([0, 1.25*maxCaf])
plt.show()
