import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
from datetime import datetime
import plotly_test as pt


"""

garden_constants.dims, garden_constants.cellsize,
                beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[u, l, bounds, num_checks]
                
"""
def generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                     utility_func, utility_postprocessing_func, test_util_exp=0, self_multiplier=1,
                                     num_each_plant=None, trialno=-1,
                                     data=None, generate_plotly=True, save_plotly=True, save=True):
    if data == None:
        data = poi.generate_garden(dims=garden_constants.dims, cellsize=garden_constants.cellsize,
                                   beta=beta, num_p_selector=num_p_selector,
                                   bounds_map_creator_args=bounds_map_creator_args,
                                   fill_final=fill_final, utility_func=utility_func,
                                   utility_postprocessing_func=utility_postprocessing_func,
                                   num_each_plant=num_each_plant)
    time_elapsed = poi.global_time_elapsed
    h = np.zeros(garden_constants.num_plants)
    num_plants_arr = np.zeros(garden_constants.num_plants)

    fig, ax = plt.subplots()
    for p in data:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))

        num_plants_arr[plant_index] += 1
    num_plants_arr_txt = [str(int(x)) for x in num_plants_arr]
    plant_index_arr = np.arange(garden_constants.num_plants)
    plant_index_arr_txt = [str(x) for x in plant_index_arr]
    table_text = [plant_index_arr_txt, num_plants_arr_txt]
    row_labels = ['plant type', 'num plant']

    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]

    ax.scatter(datax, datay, s=1, color='k')

    gxl = garden_constants.garden_x_len
    gyl = garden_constants.garden_y_len
    garden_vecs = [[0,0], [gxl, 0], [gxl, gyl], [0, gyl]]
    for i in range(-1, len(garden_vecs) - 1):
        ax.plot(garden_vecs[i], garden_vecs[i + 1], color='k')
    ax.set_aspect(1)
    ax.table(cellText=table_text,
              rowLabels=row_labels,
              loc='bottom')
    plt.subplots_adjust(hspace=0.4)
    plt.title('beta: {}; trial: {}; num plants: {}'.format(beta, trialno, data.shape[0]))
    if data.shape[0] >= 20:
        print('FOUND: beta: {}; trial: {}; num plants: {}'.format(beta, trialno, data.shape[0]))
    else:
        print('beta: {}; trial: {}; num plants: {}'.format(beta, trialno, data.shape[0]))
    if save:
        if data.shape[0] >= 20:
            fig_filename = "ag-main-winners-images/compexp_{}_selfmultiplier_{}_beta_{}_trialno_{}_numplants_{}_2d_plot_{}"\
                .format(test_util_exp, self_multiplier, int(beta * 10), trialno, data.shape[0],
                        datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
            data_filename = "ag-main-winners-data/compexp_{}_selfmultiplier_{}_beta_{}_trialno_{}_numplants_{}_data_{}"\
                .format(test_util_exp, self_multiplier, int(beta * 10), trialno, data.shape[0],
                        datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
        else:
            fig_filename = "ag-main-demos/numplants_{}_beta_{}_compexp_{}_selfmultiplier_{}_trialno_{}_2d_plot_{}"\
                .format(data.shape[0],
                int(beta * 10), test_util_exp, self_multiplier, trialno, datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
            data_filename = "ag-main-demos/numplants_{}_beta_{}_compexp_{}_selfmultiplier_{}_trialno_{}_data_{}"\
                .format(data.shape[0],
                int(beta * 10), test_util_exp, self_multiplier, trialno, datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
        plt.savefig(fig_filename, dpi=200)
        np.save(data_filename, data)
        plt.close()
    elif generate_plotly:
        pt.plotly_test(pt.single_values['y_eye_mult'],
                       pt.single_values['z_ratio'],
                       pt.single_values['h_mult'],
                       pt.single_values['color_dict'],
                       data=data, plant_labels=False, save=save_plotly)
    else:
        plt.show()
    return fig, ax

