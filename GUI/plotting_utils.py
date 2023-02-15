import matplotlib
matplotlib.use('Agg')
import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
from datetime import datetime
import plotly_test as pt
import re
import pickle


"""

garden_constants.dims, garden_constants.cellsize,
                beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[u, l, bounds, num_checks]
                
"""
def num_to_str(num):
    a = "{:.4f}".format(num)
    str_a = str(a)
    list_str_a = re.split(r'\.', str_a)
    if len(list_str_a) == 2:
        str_a = list_str_a[0] + "," + list_str_a[1]
    return str_a

dataset_no = 10
timestamp = False

def generate_garden_scatter_and_area(d, garden, cylinder_nt, image_id, num_images, trialno=-1, data=None, generate_plotly=True,
                                     save_plotly=True, save_2d=True,
                                     ):
    if data is None:
        data = poi.generate_garden(dims=garden_constants.dims, cellsize=garden_constants.cellsize, d=d)
    time_elapsed = poi.global_time_elapsed
    h = np.zeros(garden_constants.num_plants)
    num_plants_arr = np.zeros(garden_constants.num_plants)

    fig, ax = plt.subplots()
    for p in data:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        if plant_index == 0:
            r = d['void_size']
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
    ax.table(cellText=table_text,
              rowLabels=row_labels,
              loc='top')
    gxl = garden_constants.garden_x_len
    gyl = garden_constants.garden_y_len
    garden_vecs = [[0,0], [gxl, 0], [gxl, gyl], [0, gyl]]
    for i in range(-1, len(garden_vecs) - 1):
        ax.plot(garden_vecs[i], garden_vecs[i + 1], color='k')
    ax.set_aspect(1)
    ax.legend(handles=garden_constants.legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    garden_comp_score = garden_constants.garden_companionship_score(data)
    plt.suptitle('imageid: {}'.format(image_id), y=1)
    polygon = d['bmca'][0][0]
    x, y = polygon.exterior.xy
    plt.plot(x, y, 'r')
    if timestamp:
        filename = f'datasets/dataset{dataset_no}/{dataset_no}_{image_id}_{datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f")}'
    else:
        filename = f"datasets/dataset{dataset_no}/{dataset_no}_{image_id}"
    if save_2d:
        plt.savefig(filename + '_2d', dpi=200)
        # UPDATE VOID NUMBER TO ACTUAL NUBMER OF VOIDS
        garden['void_number'] = sum([(1 if x[1] == 0 else 0) for x in data])
        garden['data'] = data
        garden.pop('d')
        pickle.dump(garden, open(f'{filename}_data', "wb" ))
        plt.close()
        print(f'image_id {image_id} out of {num_images - 1}')
    print("printing the plot")
    # if generate_plotly:
    #     pt.plotly_test(pt.single_values['y_eye_mult'],
    #                    pt.single_values['z_ratio'],
    #                    pt.single_values['h_mult'],
    #                    pt.single_values['color_dict'],
    #                    cylinder_nt=cylinder_nt,
    #                    data=data, plant_labels=False, save=save_plotly,
    #                    where_to_save=filename, void_size=garden['void_size'])
    # else:
    #     plt.show()
    return fig, ax

