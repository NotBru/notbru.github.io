import matplotlib.pyplot as plt
import numpy as np

def plot_dot(ax, x, y, color=(1, 1, 1)):
    ax.scatter([x], [y], color=(.2, .2, .2), s=50, zorder=1)
    ax.scatter([x], [y], color=color, s=20, zorder=2)

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("Amount of X")
ax.set_ylabel("Amount of Y")
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)

ls = np.linspace(0, 1, 5)[1:]
for l in ls:
    x = np.linspace(0, 1, 128)
    y = l ** 2 / x
    ax.plot(x, y, color=(.2, .2, .2), ls='-')

ps = 2 ** np.linspace(-3, 3, 5)
for p in ps:
    x = np.linspace(0, 1, 128)
    y = p * x
    ax.plot(x, y, color=(.2, .2, .2), ls='--')

fig.savefig("fig01.png")
