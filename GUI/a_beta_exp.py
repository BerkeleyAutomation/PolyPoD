import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
import math
import re

dims = np.array([garden_constants.garden_x_len, garden_constants.garden_y_len])
garden_area = np.prod(dims)
cellsize=0.1
x = 2

def vrpd_scatter_and_area(a, beta, num_p_selector, trialno, show=False, save=False):
    data = poi.vrpd(dims=dims, cellsize=cellsize,
                    beta=beta, a=a, num_p_selector=num_p_selector)
    ax = plt.gca()
    h = np.zeros(garden_constants.num_plants)
    num_plants_arr = np.zeros(garden_constants.num_plants)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    for p in data:
        loc, plant_index = p
        plant_index = int(plant_index)
        r = garden_constants.plant_radii[plant_index]
        color = garden_constants.colors_of_plants_hi_contrast[int(plant_index)]
        ax1.add_patch(plt.Circle(loc, r, color=color, fill=False, clip_on=False))

        area = math.pi * (garden_constants.plant_radii[plant_index] ** 2)
        h[plant_index] += area
        num_plants_arr[plant_index] += 1
    num_plants_arr_txt = [str(int(x)) for x in num_plants_arr]
    plant_index_arr = np.arange(garden_constants.num_plants)
    plant_index_arr_txt = [str(x) for x in plant_index_arr]
    table_text = [plant_index_arr_txt, num_plants_arr_txt]
    row_labels = ['plant type', 'num plant']
    h_sum = np.sum(h)
    h_sum_txt = "{:.4f}".format(h_sum)
    h /= h_sum
    locdata = np.array([p[0] for p in data])
    datax, datay = locdata[:,0], locdata[:,1]

    ax1.scatter(datax, datay, s=1, color='k')
    gxl = garden_constants.garden_x_len
    gyl = garden_constants.garden_y_len
    garden_vecs = [[0,0], [gxl, 0], [gxl, gyl], [0, gyl]]
    for i in range(-1, len(garden_vecs) - 1):
        ax1.plot(garden_vecs[i], garden_vecs[i + 1], color='k')
    ax1.set_title('Image')
    ax2.bar(plant_index_arr, h)
    ax2.set_xticks([])
    ax2.table(cellText=table_text,
              rowLabels=row_labels,
              loc='bottom')
    ax2.set_ylabel('Fraction of total area')
    ax2.set_title('Plant area distribution / num each plant\nActual total area used: {0}'.format(h_sum_txt))
    plt.subplots_adjust(wspace=0.4)

    str_a, str_beta = a_beta_to_str(a, beta)

    titlename = "a/beta experiment: a={0}, beta={1}, trial {2}".format(a, beta, trialno)
    fig.suptitle(titlename, y=1.0)
    ax1.set_aspect(1)
    if save:
        fig_filename = "a_beta_exp/a_beta_exp_a{0}_beta{1}_trial{2}".format(str_a, str_beta, trialno)
        plt.savefig(fig_filename, dpi=200)
        data_filename = "a_beta_exp/data/a_beta_exp_a{0}_beta{1}_trial{2}_data"\
            .format(str_a, str_beta, trialno)
        np.save(data_filename, data)
    if show:
        plt.show()
    return plant_index_arr, h, plant_index_arr_txt, h_sum, num_plants_arr

a_list = np.arange(0.5, 2.1, 0.1)
beta_list = np.arange(0, 1.1, 0.1)
notrials=10
def a_beta_exp(a_list, beta_list, notrials):
    for beta in beta_list:
        for a in a_list:
            master_h = np.zeros(garden_constants.num_plants, dtype=np.float32)
            master_h_sum = 0
            master_num_plants_arr = np.zeros(garden_constants.num_plants)
            plant_index_arr, h, plant_index_arr_txt, h_sum, num_plants_arr = [None, None, None, None, None]
            for t in range(notrials):
                plant_index_arr, h, plant_index_arr_txt, h_sum, num_plants_arr = \
                    vrpd_scatter_and_area(a=a, beta=beta, trialno=t, show=False, save=True,
                                          num_p_selector=poi.weighted_round_or_one)
                master_h += h
                master_h_sum += h_sum
                master_num_plants_arr += num_plants_arr
            master_h /= notrials
            master_h_sum /= notrials
            master_h_sum_txt = "{:.4f}".format(master_h_sum)
            master_num_plants_arr /= notrials
            fig, ax = plt.subplots()
            ax.bar(plant_index_arr, master_h)
            ax.set_xticks([])
            master_num_plants_arr_txt = np.array(["{:.2f}".format(x) for x in master_num_plants_arr])
            table_text = [plant_index_arr_txt, master_num_plants_arr_txt]
            row_labels = ['plant type', 'avg num plants']
            ax.table(cellText=table_text,
                      rowLabels=row_labels,
                      loc='bottom')
            ax.set_ylabel('Avg Fraction of total area')
            ax.set_title('Avg Plant area distribution / avg num each plant for '
                         'a={0}, beta={1}, {3} trials\nActual Avg total area used: {2}'
                         .format(a, beta, master_h_sum_txt, notrials))
            str_a, str_beta = a_beta_to_str(a, beta)
            fig_filename = "a_beta_exp/avg_area_hists/a_beta_exp_avg_hist_a{0}_beta{1}"\
                .format(str_a, str_beta)
            plt.savefig(fig_filename, dpi=180, bbox_inches="tight", pad_inches=0.25)

def a_beta_to_str(a, beta):
    str_a = str(a)
    list_str_a = re.split(r'\.', str_a)
    if len(list_str_a) == 2:
        str_a = list_str_a[0] + "," + list_str_a[1]
    str_beta = str(beta)
    list_str_beta = re.split(r'\.', str_beta)
    if len(list_str_beta) == 2:
        str_beta = list_str_beta[0] + "," + list_str_beta[1]
    return str_a, str_beta

a_beta_exp([0.7, 1.4], [0, 1], 2)