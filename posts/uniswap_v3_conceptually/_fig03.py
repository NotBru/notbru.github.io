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

ps = [1/10, 1/3, 1/2, 1/1.2, 1.2,  2,  3, 10]
ls = [.2, .5,    .9,   1, .9, .5, .2]
for pi, pf, l in zip(ps[:-1], ps[1:], ls):
    xi = l / pi ** .5
    xf = l / pf ** .5
    x = np.linspace(xi, xf, 128)
    y = l ** 2 / x
    yi, yf = y[0], y[-1]
    ax.plot(x, y, color=(0, 0, 0), ls='-')

for p in ps:
    x = np.array([0, 2])
    y = p * x
    ax.plot(x, y, color=(.5, .5, .5), ls='-.', lw=.8, zorder=-1)
for l in ls:
    x = np.linspace(0, 2, 128)
    y = l ** 2 / x
    ax.plot(x, y, color=(.75, .75, .75), ls='-.', lw=.8, zorder=-1)

"""
ps = [0] + ps + [0]
ls = [0] + ls + [0]
for p, li, lf in zip(ps[1:], ls[:-1], ls[1:]):
    xi, xf = li / p ** .5, lf / p ** .5
    yi, yf = li * p ** .5, lf * p ** .5
    ax.plot([xi, xf], [yi, yf], color=(.2, .2, .2), ls='--')
"""

fig.savefig("fig03.png", dpi=400)
