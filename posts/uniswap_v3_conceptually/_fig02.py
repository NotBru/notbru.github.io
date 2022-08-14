import matplotlib.pyplot as plt
import numpy as np

def plot_dot(ax, x, y, color=(1, 1, 1)):
    ax.scatter([x], [y], color=(.2, .2, .2), s=50, zorder=1)
    ax.scatter([x], [y], color=color, s=20, zorder=2)

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_xlabel("Amount of X")
ax.set_ylabel("Amount of Y")
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)

l = 1
x = np.linspace(1/1.5, 1.5, 128)
y = l ** 2 / x
ax.plot(x, y, color=(0, 0, 0), ls='-')
ax.plot([0, x[0]], [0, y[0]], color=(.2, .2, .2), ls='--', lw=.8)
ax.plot([0, x[-1]], [0, y[-1]], color=(.2, .2, .2), ls='--', lw=.8)
plot_dot(ax, 1, 1, color=(.6, .3, .2))

fig.savefig("fig02.png", dpi=400)
