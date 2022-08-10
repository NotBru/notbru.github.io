import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 6))
x = np.linspace(0, 1, 128)
y = 1 / x
ax.plot(x, y)
fig.savefig("_fig00.png")
