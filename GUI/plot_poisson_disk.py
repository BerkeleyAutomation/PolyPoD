import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np

r = 0.25
dims = np.array([garden_constants.garden_x_len, garden_constants.garden_y_len])
num_of_each_plant = np.full(garden_constants.num_plants, 3)
plant_radii = garden_constants.plant_height_distribution_params
cellsize=0.1
data = poi.vrpd(dims, num_of_each_plant, plant_radii, cellsize)
ax = plt.gca()
for p in data:
    loc, plant_index = p
    r = garden_constants.plant_height_distribution_params[plant_index]
    color = garden_constants.colors_of_plants[int(plant_index)]
    ax.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))
locdata = np.array([x[0] for x in data])
datax, datay = locdata[:,0], locdata[:,1]
plt.scatter(datax, datay, s=1, color='k')
ax.set_aspect(1)
plt.show()