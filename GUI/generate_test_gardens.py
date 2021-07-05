import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np

beta = 1
self_beta = 0
void_beta = -6
num_trials = 1000
num_p_selector = poi.weighted_round_or_one
fill_final = True
data = None #np.load('french_plots/data_06-08-21_19-18-07-814772.npy', allow_pickle=True)
generate_plotly=False
save_plotly=False
save=True
# util_func = False
num_each_plant = np.full(9, 2, dtype='int')
planting_order = [0, 8, 7, 6, 5, 4, 3, 2, 1]
#num_each_plant[9] = 2
comp_exps = [2]
self_multipliers = [1] #[2, 4, 8]
from numpy.random import default_rng
from numpy.random import choice
rng = default_rng()

#bounds_map_creator_args = french_gardens_utils.french_demo_bac()
#bounds_map_creator_args = [[lambda x: 4, lambda x: 0, [0, 4, 0, 4]]]
bounds_map_creator_args = False
# Probably should place both void plants! [type 0]
def void_centers(r):
    p2 = 141.42 - (2/3) * r
    p1 = (1/2) * p2 - r
    c1 = p1 + r
    c2 = p2 + r
    c1_xy = c1 / math.sqrt(2)
    c2_xy = c2 / math.sqrt(2)
    centers = [[c1_xy, c1_xy], [c2_xy, c2_xy]]
    return centers

v_centers = void_centers(garden_constants.void_radius)

starting_plants_dict = {-1: [],
                    0: [[v_centers[0], 0], [v_centers[1], 0]],
                   1: [[[75, 75], 9]],
                   2: [[[35, 35], 9], [[115, 115], 9]],
                   3: [[[35, 55], 9], [[115, 95], 9]],
                   4: [[[55, 55], 9], [[95, 95], 9]]
                   }
starting_configs = [-1]
def random_ps(candidates, plant_type, added_points):
    draw = candidates[rng.integers(candidates.shape[0])]
    return [draw[0], draw[1]]

for comp_exp in comp_exps:
    for self_multiplier in self_multipliers:
        for sp_index in starting_configs:
            for t in range(num_trials):
                #print('comp_exp: ', comp_exp, '; self_multiplier: ', self_multiplier,
                #      '; sp_index ', sp_index, '; trial: ', t)
                starting_plants = starting_plants_dict[sp_index]

                utility_func = lambda p, plant_type, added_points: garden_constants.point_companionship_score(
                    p, plant_type, added_points, self_multiplier
                )
                utility_postprocessing_func = lambda pd: garden_constants.comp_pd_postprocessing(pd, comp_exp)
                def comp_ps(candidates, plant_type, added_points):
                    probability_distribution = np.array([utility_func([p[0], p[1]], plant_type,
                                                                      added_points) for p in candidates])
                    if utility_postprocessing_func is not None:
                        #print('1 probability distribution before postprocessing: {}'.format(probability_distribution))
                        probability_distribution = utility_postprocessing_func(probability_distribution)
                        #print('2 probability distribution after postprocessing: {}'.format(probability_distribution))
                    pd_sum = probability_distribution.sum()
                    if pd_sum > 0:
                        #print('3 probability distribution before dividing by pd_sum. pd_sum: {}; probability distribution: {}'
                        #      .format(pd_sum, probability_distribution))
                        probability_distribution = probability_distribution / pd_sum
                        #print('4 probability distribution after dividing by pd_sum. pd_sum: {}; probability distribution: {}'
                        #      .format(pd_sum, probability_distribution))
                    else:
                        probability_distribution = np.ones(
                            probability_distribution.shape) / probability_distribution.shape
                    selection_array = np.arange(len(candidates))
                    #print('candidates {}\nplant type {}\nadded_points {}\nprobability distribution {}\n~\n'.format(
                    #    candidates, plant_type, added_points, probability_distribution))
                    draw_num = choice(selection_array, 1,
                                      p=probability_distribution)
                    draw = candidates[draw_num]
                    return [draw[0][0], draw[0][1]]

                plotting_utils.generate_garden_scatter_and_area(beta=beta, num_p_selector=num_p_selector,
                                                                bounds_map_creator_args=bounds_map_creator_args,
                                                                fill_final=fill_final,
                                                                self_beta=self_beta, void_beta=void_beta,
                                                                data=data, generate_plotly=generate_plotly,
                                                                comp_exp=comp_exp, self_multiplier=self_multiplier,
                                                                next_point_selector=comp_ps,
                                                                save_plotly=save_plotly, save=save,
                                                                num_each_plant=num_each_plant, trialno=t,
                                                                starting_plants=starting_plants,
                                                                sp_index=sp_index, planting_order=planting_order)
