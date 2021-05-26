import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
from datetime import datetime


"""

garden_constants.dims, garden_constants.cellsize,
                beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[u, l, bounds, num_checks]
                
"""
def generate_garden_scatter_and_area(a, beta, num_p_selector, bounds_map_creator_args,
                                     show=False, save=False):
    data = poi.generate_garden(dims=garden_constants.dims, cellsize=garden_constants.cellsize,
                               beta=beta, a=a, num_p_selector=num_p_selector,
                               bounds_map_creator_args=bounds_map_creator_args)
    h = np.zeros(garden_constants.num_plants)
    num_plants_arr = np.zeros(garden_constants.num_plants)

    fig, ax = plt.subplots()
    for p in data:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))
    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]

    ax.scatter(datax, datay, s=1, color='k')

    gxl = garden_constants.garden_x_len
    gyl = garden_constants.garden_y_len
    garden_vecs = [[0,0], [gxl, 0], [gxl, gyl], [0, gyl]]
    for i in range(-1, len(garden_vecs) - 1):
        ax.plot(garden_vecs[i], garden_vecs[i + 1], color='k')
    ax.set_aspect(1)
    if save:
        fig_filename = "test_plots/plotted_graph_{0}".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
        plt.savefig(fig_filename, dpi=200)
        data_filename = "test_plots/plotted_graph_data_{0}".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
        np.save(data_filename, data)
    if show:
        plt.show()
    return fig, ax