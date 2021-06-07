import french_gardens_utils
import numpy as np
import matplotlib.pyplot as plt

b = french_gardens_utils.bounds_map_creator_args
step = 0.1
datax = []
datay = []
for bmca in b:
    upper, lower, bounds, num_checks = bmca
    for n in np.arange(bounds[0], bounds[1], step):
        datax.extend([n, n])
        datay.extend([upper(n), lower(n)])
plt.scatter(datax, datay, s=2)
plt.show()