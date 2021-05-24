import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
import math
import re

def generate_garden_scatter_and_area(a, beta, num_p_selector, trialno, show=False, save=False):
    data = poi.generate_garden(dims=garden_constants.dims, cellsize=garden_constants.cellsize,
                    beta=beta, a=a, num_p_selector=num_p_selector)
    ax = plt.gca()
    h = np.zeros(garden_constants.num_plants)
    num_plants_arr = np.zeros(garden_constants.num_plants)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    for p in data:
        loc, plant_index, r = poi.point_unpacker(p)
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax1.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))
    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]

    ax1.scatter(datax, datay, s=1, color='k')

    gxl = garden_constants.garden_x_len
    gyl = garden_constants.garden_y_len
    garden_vecs = [[0,0], [gxl, 0], [gxl, gyl], [0, gyl]]
    for i in range(-1, len(garden_vecs) - 1):
        ax1.plot(garden_vecs[i], garden_vecs[i + 1], color='k')
    ax1.set_aspect(1)
    if save:
        fig_filename = "plotted_graph"
        plt.savefig(fig_filename, dpi=200)
        data_filename = "plotted_graph_data"
        np.save(data_filename, data)
    if show:
        plt.show()