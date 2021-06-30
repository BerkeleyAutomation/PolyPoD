import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np

betas = [0.7, 0.8, 0.9, 1]
num_trials = 30
num_p_selector = poi.weighted_round_or_one
fill_final = True
data = None #np.load('french_plots/data_06-08-21_19-18-07-814772.npy', allow_pickle=True)
generate_plotly=False
save_plotly=False
save=True
use_util_func = False
num_each_plant = 2
util_exps = [1]
self_multipliers = [1]

#bounds_map_creator_args = french_gardens_utils.french_demo_bac()
#bounds_map_creator_args = [[lambda x: 4, lambda x: 0, [0, 4, 0, 4]]]
bounds_map_creator_args = False
for util_exp in util_exps:
    def comp_util(p, plant_type, points, added_points):
        return garden_constants.companionship_score(p, plant_type, points, added_points, exp=exp, self_multiplier=self)
    for beta in betas:
        for t in range(num_trials):
            plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                            utility_func=use_util_func,
                                                            test_util_exp=util_exp,
                                                            data=data, generate_plotly=generate_plotly,
                                                            save_plotly=save_plotly, save=save,
                                                            num_each_plant=num_each_plant, trialno=t)
