import numpy as np
import matplotlib.pyplot as plt
#!!! you may need to execute this cell twice in order to see the output due to an problem with matplotlib
x = np.arange(0., 30.0)
y = 1-(3/4)**x
fig, ax = plt.subplots(nrows = 1, ncols = 1)
fig = plt.figure()
fig.patch.set_facecolor('#2F303A')
ax = fig.add_subplot(1,1,1)
plt.plot(y)
plt.title('Probablity of you detecting Eve - The Hacker')
plt.xlabel('# of key bits compared')
ax = plt.gca()
ax.set_facecolor('#2F303A')
ax.xaxis.label.set_color('white')
ax.title.set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

plt.show()
