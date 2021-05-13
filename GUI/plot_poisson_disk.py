import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np

r = 0.25
dims = np.array([garden_constants.garden_x_len, garden_constants.garden_y_len])
num_of_each_plant = np.full(garden_constants.num_plants, 2)
plant_radii = garden_constants.plant_height_distribution_params
cellsize=0.1
data = poi.vrpd(dims, num_of_each_plant, plant_radii, cellsize)
ax = plt.gca()
for p in data:
    ax.add_patch(plt.Circle(p, r, color='b', fill=False, clip_on=False))
datax, datay = data[:,0], data[:,1]
plt.scatter(datax, datay, s=1, color='k')
ax.set_aspect(1)
plt.show()