import matplotlib.pyplot as plt
import numpy as np

def plot_dot(ax, x, y, color=(1, 1, 1)):
    ax.scatter([x], [y], color=(.2, .2, .2), s=50, zorder=1)
    ax.scatter([x], [y], color=color, s=20, zorder=2)

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
idxi = 20
idxf = 50
xi, yi = x[idxi], y[idxi]
xf, yf = x[idxf], y[idxf]

ax.plot(x, y, c="k", zorder=0)
plot_dot(ax, xi, yi, (0, .5, .8))
plot_dot(ax, xf, yf, (0, .8, .3))
ax.plot([xi, xf], [yi, yi], c=(.2, .2, .2), ls='--', zorder=-1)
ax.text(.35 * xi + .5 * xf, yi * 1.05, "Δx")
ax.plot([xf, xf], [yi, yf], c=(.2, .2, .2), ls='--', zorder=-1)
ax.text(xf * 1.05, .48 * yi + .5 * yf, "Δy")
fig.savefig("fig00.png")
