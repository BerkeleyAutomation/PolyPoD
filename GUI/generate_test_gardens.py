import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np

betas = [0.9, 1]
num_trials = 10
num_p_selector = poi.weighted_round_or_one
fill_final = True
data = None #np.load('french_plots/data_06-08-21_19-18-07-814772.npy', allow_pickle=True)
generate_plotly=False
save_plotly=False
save=True
# util_func = False
num_each_plant = 2
comp_exps = [-1, -3, -8]
self_multipliers = [1, 3, 8]

#bounds_map_creator_args = french_gardens_utils.french_demo_bac()
#bounds_map_creator_args = [[lambda x: 4, lambda x: 0, [0, 4, 0, 4]]]
bounds_map_creator_args = False
for comp_exp in comp_exps:
    for self_multiplier in self_multipliers:
        def util_func(p, plant_type, points, added_points):
            return garden_constants.companionship_score(p, plant_type, points, added_points,
                                                        exp=comp_exp, self_multiplier=self_multiplier)
        for beta in betas:
            for t in range(num_trials):
                plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                                utility_func=util_func,
                                                                test_util_exp=comp_exp, self_multiplier=self_multiplier,
                                                                data=data, generate_plotly=generate_plotly,
                                                                save_plotly=save_plotly, save=save,
                                                                num_each_plant=num_each_plant, trialno=t)
