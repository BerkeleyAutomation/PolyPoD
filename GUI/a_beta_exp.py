import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
import math

dims = np.array([garden_constants.garden_x_len, garden_constants.garden_y_len])
cellsize=0.1
x = 2

def vrpd_scatter_and_area(a, beta, show=False, save=False):
    data = poi.vrpd(dims=dims, cellsize=cellsize,
                    x=x, beta=beta, a=a)
    ax = plt.gca()
    h = np.zeros(garden_constants.num_plants)
    for p in data:
        loc, plant_index = p
        r = garden_constants.plant_radii[plant_index]
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))

        area = math.pi * (garden_constants.plant_radii[plant_index] ** 2)
        h[plant_index] += area
    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]
    plt.scatter(datax, datay, s=1, color='k')
    titlename = "a/beta exp: a={0}, beta={1}".format(a, beta)
    plt.title(titlename)
    ax.set_aspect(1)
    if save:
        filename = "a_beta_exp/a_beta_exp_a{0}_beta{1}".format(a, beta)
        plt.savefig(filename)
    if show:
        plt.show()
    return h

vrpd_scatter_and_area(1, 0, show=True, save=True)