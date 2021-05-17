import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
import math
import re

dims = np.array([garden_constants.garden_x_len, garden_constants.garden_y_len])
cellsize=0.1
x = 2

def vrpd_scatter_and_area(a, beta, show=False, save=False):
    data = poi.vrpd(dims=dims, cellsize=cellsize,
                    beta=beta, a=a)
    ax = plt.gca()
    h = np.zeros(garden_constants.num_plants)
    for p in data:
        loc, plant_index = p
        plant_index = int(plant_index)
        r = garden_constants.plant_radii[plant_index]
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))

        area = math.pi * (garden_constants.plant_radii[plant_index] ** 2)
        h[plant_index] += area
    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]
    plt.scatter(datax, datay, s=1, color='k')
    plt.plot([0,0], [10,0], color='k')
    plt.plot([10, 0], [10, 10], color='k')
    plt.plot([10, 10], [0, 10], color='k')
    plt.plot([0, 10], [0, 0], color='k')

    str_a = str(a)
    list_str_a = re.split(r'\.', str_a)
    if len(list_str_a) == 2:
        str_a = list_str_a[0] + "," + list_str_a[1]
    str_beta = str(beta)
    list_str_beta = re.split(r'\.', str_beta)
    if len(list_str_beta) == 2:
        str_beta = list_str_beta[0] + "," + list_str_beta[1]

    titlename = "a/beta experiment: a={0}, beta={1}".format(a, beta)
    plt.title(titlename)
    ax.set_aspect(1)
    if save:
        filename = "a_beta_exp/a_beta_exp_a{0}_beta{1}".format(str_a, str_beta)
        plt.savefig(filename)
    if show:
        plt.show()
    return h

vrpd_scatter_and_area(a=2, beta=0, show=True, save=True, num_p_selector=poi.weighted_round)