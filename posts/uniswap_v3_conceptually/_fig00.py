import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, 128)
ax.set_xlabel("Amount of X")
ax.set_ylabel("Amount of Y")
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)

k = 10
x = np.linspace(0, 1, 128)
y = k / x
idx = 20
x_dot = x[idx:idx+1]
y_dot = y[idx:idx+1]

ax.plot(x, y, c="k", zorder=0)
ax.scatter(x_dot, y_dot, color=(.2, .2, .2), s=50, zorder=1)
ax.scatter(x_dot, y_dot, color=(0, .8, .3), s=20, zorder=2)
fig.savefig("fig00.png")
