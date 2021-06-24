import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np

beta = 1
num_p_selector = poi.weighted_round_or_one
fill_final = False
data = False #np.load('french_plots/data_06-08-21_19-18-07-814772.npy', allow_pickle=True)
save_plotly=False
show=True
save=False
util_exp = -3
test_util_exps = [1]

#bounds_map_creator_args = french_gardens_utils.french_demo_bac()
#bounds_map_creator_args = [[lambda x: 4, lambda x: 0, [0, 4, 0, 4]]]
bounds_map_creator_args = False
for test_util_exp in test_util_exps:
    def similar_clustering_utility_func(p, plant_type, points, added_points):
        cum_dist = 0
        for o in added_points[plant_type]:
            pass
            o_loc = o[0]
            cum_dist += math.dist(p, o_loc)
        if cum_dist == 0:
            return 1
        else:
            return cum_dist ** test_util_exp
    plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                    utility_func=False,
                                                    test_util_exp=test_util_exp,
                                                    data=data, save_plotly=save_plotly, show=show, save=save)