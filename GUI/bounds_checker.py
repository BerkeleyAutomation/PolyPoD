import french_gardens_utils
import numpy as np
import matplotlib.pyplot as plt

b = french_gardens_utils.french_demo_bac()
step = 0.1
dataxu = []
datayu = []
dataxl = []
datayl = []
for bmca in b:
    upper, lower, bounds, num_checks = bmca
    for n in np.arange(bounds[0], bounds[1], step):
        dataxu.append(n)
        datayu.append(upper(n))
        dataxl.append(n)
        datayl.append(lower(n))
plt.scatter(dataxu, datayu, color='blue', s=2)
plt.scatter(dataxl, datayl, color='red', s=2)
plt.show()