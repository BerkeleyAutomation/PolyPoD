import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np
from numpy.random import default_rng
from numpy.random import choice
rng = default_rng()

# GENERAL VARIABLES: SET
num_trials = 5
num_p_selector = poi.weighted_round_or_one
data = None
cylinder_nt = 70
generate_plotly=True
save_plotly=True
save_2d=True
void_beta = -6
def random_ps(candidates, plant_type, added_points):
    draw = candidates[rng.integers(candidates.shape[0])]
    return [draw[0], draw[1]]
def next_point_selector_with_utility_func(candidates, plant_type, added_points, utility_func):
    if utility_func is None:
        return random_ps(candidates, plant_type, added_points)
    probability_distribution = np.array([utility_func([p[0], p[1]], plant_type,
                                                      added_points) for p in candidates])
    pd_sum = probability_distribution.sum()
    if pd_sum > 0:
        probability_distribution = probability_distribution / pd_sum
    else:
        probability_distribution = np.ones(
            probability_distribution.shape) / probability_distribution.shape
    selection_array = np.arange(len(candidates))
    draw_num = choice(selection_array, 1,
                      p=probability_distribution)
    draw = candidates[draw_num]
    return [draw[0][0], draw[0][1]]

# LIST OF ALL EXPERIMENTAL VARIABLES
all_variables = []

# EXPERIMENTAL VARIABLE INITIATION
beta_name = 'beta'
beta_values = [0, 0.2, 0.4, 0.6, 0.8, 1]
def include_beta(d, v):
    return True
def beta_func(d, v):
    return v
all_variables.append([beta_name, beta_values, include_beta, beta_func])

self_beta_name = 'self_beta'
self_beta_values = [0, 'same']
def include_self_beta(d, v):
    return True
def self_beta_func(d, v):
    if v == 0:
        return 0
    elif v == 'same':
        return d['beta']
all_variables.append([self_beta_name, self_beta_values, include_self_beta, self_beta_func])

utility_func_exponent_name = 'utility_func_exponent'
utility_func_exponent_values = [-8, -5, -4, -3, None]
def include_utility_func_exponent(d, v):
    return True
def utility_func_exponent_func(d, v):
    return v
all_variables.append([utility_func_exponent_name, utility_func_exponent_values, include_utility_func_exponent, utility_func_exponent_func])

planting_groups_name = 'planting_groups'
planting_groups_values = [[[0], [8], [7], [6], [5], [4], [3], [2], [1]],
                          [[0], [8, 4], [7, 3], [6, 2], [5, 1]]]
def include_planting_groups(d, v):
    return True
def planting_groups_func(d, v):
    return v
all_variables.append([planting_groups_name, planting_groups_values, include_planting_groups, planting_groups_func])

next_point_selector_name = 'next_point_selector'
next_point_selector_values = ['same', 'pairs', 'none']
def include_next_point_selector(d, v):
    if d['planting_groups'] == [[0], [8], [7], [6], [5], [4], [3], [2], [1]] and (v == 'same' or v == 'none'):
        return True
    elif d['planting_groups'] == [[0], [8, 4], [7, 3], [6, 2], [5, 1]] and v == 'pairs':
        return True
    else:
        return False
def next_point_selector_func(d, v):
    def clustering_utility_func(p, plant_type, other_plant_type, added_points):
        cum_dist = 0
        for o in added_points[other_plant_type]:
            pass
            o_loc = o[0]
            cum_dist += math.dist(p, o_loc)
        if cum_dist == 0:
            return 1
        else:
            return cum_dist ** d['utility_func_exponent']
    if v == 'none':
        return random_ps
    elif v == 'same':
        return lambda candidates, plant_type, added_points:\
            next_point_selector_with_utility_func(candidates, plant_type, added_points,
                                                  lambda p, plant_type, added_points:
                                                  clustering_utility_func(p, plant_type, plant_type, added_points))
    elif v == 'pairs':
        def nps(candidates, plant_type, added_points):
            planting_groups = d['planting_groups']
            other_plant_type = None
            for g in planting_groups:
                if plant_type in g:
                    gc = g.copy()
                    g.remove(v)
                    other_plant_type = g[0]
            assert other_plant_type is not None
            return next_point_selector_with_utility_func(candidates, plant_type, added_points,
                                                  lambda p, plant_type, added_points:
                                                  clustering_utility_func(p, plant_type, other_plant_type, added_points))
all_variables.append([next_point_selector_name, next_point_selector_values, include_next_point_selector,
                      next_point_selector_func])

void_size_name = 'void_size'
void_size_values = [5, 10, 15]
def include_void_size(d, v):
    return True
def void_size_func(d, v):
    return v
all_variables.append([void_size_name, void_size_values, include_void_size, void_size_func])

void_number_name = 'void_number'
void_number_values = [0, 1, 2, 3, 4]
def include_void_number(d, v):
    return True
def void_number_func(d, v):
    return v
all_variables.append([void_number_name, void_number_values, include_void_number, void_number_func])

fill_final_name = 'fill_final'
fill_final_values = [True, False]
def include_fill_final(d, v):
    return True
def fill_final_func(d, v):
    return v
all_variables.append([fill_final_name, fill_final_values, include_fill_final, fill_final_func])

print(len(all_variables))
assert False
num_each_plant = np.full(9, 100, dtype='int')
num_each_plant[0] = 0
winner_number_plants = np.sum(num_each_plant)
bounds_map_creator_args = [french_gardens_utils.french_demo_bac()]

# GENERAL VARIABLE ADDER FUNCTION
def variable_adder(l, variable):
    variable_name, variable_values, include_variable, variable_func = variable
    nl = []
    for d in l:
        for v in variable_values:
            if include_variable(d, v):
                d = d.copy()
                d[variable_name] = variable_func(d, v)
                nl.append(d)
    return nl

# THE COMBO LIST
l = [{}]

# ADDING VARIABLES TO COMBO LIST
for variable in all_variables:
    l = variable_adder(l, variable)

# UNDER DEVELOPMENT
'''
def utility_func(p, t, added_points):
    pass

                    for t in range(num_trials):
                        #print('comp_exp: ', comp_exp, '; self_multiplier: ', self_multiplier,
                        #      '; sp_index ', sp_index, '; trial: ', t)
                        starting_plants = starting_plants_dict[sp_index]

                        plotting_utils.generate_garden_scatter_and_area(beta=beta, num_p_selector=num_p_selector,
                                                                        bounds_map_creator_args=bmca,
                                                                        fill_final=fill_final,
                                                                        cylinder_nt=cylinder_nt,
                                                                        self_beta=self_beta, void_beta=void_beta,
                                                                        data=None, generate_plotly=generate_plotly,
                                                                        comp_exp=comp_exp, self_multiplier=self_multiplier,
                                                                        next_point_selector=comp_ps,
                                                                        save_plotly=save_plotly, save_2d=save_2d,
                                                                        num_each_plant=num_each_plant, trialno=t,
                                                                        starting_plants=starting_plants,
                                                                        sp_index=sp_index, planting_order=planting_order,
                                                                        winner_number_plants=winner_number_plants)
'''