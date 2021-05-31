import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt
import garden_constants
import numpy as np
import math
import re

# Note: this file has produced the data it was intended to, and may not work exactly as intended anymore!

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

        area = math.pi * (garden_constants.plant_radii[plant_index] ** 2)
        h[plant_index] += area
        num_plants_arr[plant_index] += 1
    num_plants_arr_txt = [str(int(x)) for x in num_plants_arr]
    plant_index_arr = np.arange(garden_constants.num_plants)
    plant_index_arr_txt = [str(x) for x in plant_index_arr]
    table_text = [plant_index_arr_txt, num_plants_arr_txt]
    row_labels = ['plant type', 'num plant']
    h_sum = np.sum(h)
    actual_a = h_sum / garden_constants.garden_area
    actual_a_txt = "{:.4f}".format(actual_a)
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
    ax2.set_title('Plant area distribution / num each plant\nActual total area used: {0}'
                  .format(actual_a))
    plt.subplots_adjust(wspace=0.4)

    str_beta = num_to_str(beta)
    str_a = num_to_str(a)

    titlename = "a/beta experiment: a={0}, beta={1}, trial {2}".format(a, str_beta, trialno)
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
def a_beta_exp(beta_list, notrials):
    final_a_arr = np.array([])
    for beta in beta_list:
        master_h = np.zeros(garden_constants.num_plants, dtype=np.float32)
        master_h_sum = 0
        h_sum_arr = np.array([])
        trials_arr = np.arange(notrials)
        master_num_plants_arr = np.zeros(garden_constants.num_plants)
        plant_index_arr, h, plant_index_arr_txt, h_sum, num_plants_arr = [None, None, None, None, None]
        a = 2
        for t in range(notrials):
            plant_index_arr, h, plant_index_arr_txt, h_sum, num_plants_arr = \
                generate_garden_scatter_and_area(a=a, beta=beta, trialno=t, show=False, save=True,
                                      num_p_selector=poi.weighted_round_or_one)
            master_h += h
            master_h_sum += h_sum
            master_num_plants_arr += num_plants_arr
            h_sum_arr = np.append(h_sum_arr, h_sum / garden_constants.garden_area)
            a = h_sum / garden_constants.garden_area
        final_a_arr = np.append(final_a_arr, a)
        master_h /= notrials
        master_h_sum /= notrials
        master_h_sum_txt = "{:.4f}".format(master_h_sum)
        master_num_plants_arr /= notrials

        fig, ax = plt.subplots()
        ax.scatter(trials_arr, h_sum_arr)
        ax.set_ylabel('h_sum')
        ax.set_title('h_sum [next a value] for each trial: '
                     'beta={0}, {1} trials'
                     .format(beta, notrials))
        str_beta = num_to_str(beta)
        fig_filename = "a_beta_exp/avg_area_hists/a_beta_exp_h_sum_hist_beta{0}"\
            .format(str_beta)
        plt.savefig(fig_filename, dpi=180, bbox_inches="tight", pad_inches=0.25)
    fig, ax = plt.subplots()
    ax.scatter(beta_list, final_a_arr)
    ax.set_ylabel('final a')
    ax.set_xlabel('beta')
    ax.set_title('final a for each beta')
    fig_filename = "a_beta_exp/avg_area_hists/final_a_hist"
    plt.savefig(fig_filename, dpi=180, bbox_inches="tight", pad_inches=0.25)

def num_to_str(num):
    a = "{:.2f}".format(num)
    str_a = str(a)
    list_str_a = re.split(r'\.', str_a)
    if len(list_str_a) == 2:
        str_a = list_str_a[0] + "," + list_str_a[1]
    return str_a

a_beta_exp([0], 1)