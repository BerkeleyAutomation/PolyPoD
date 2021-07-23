import bmca_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np
from numpy.random import default_rng
from numpy.random import choice
rng = default_rng()
import random

# GENERAL VARIABLES: SET
num_trials = 1
num_p_selector = poi.weighted_round_or_one
data = None
cylinder_nt = 70
generate_plotly=False
save_plotly=False
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

# EXPERIMENTAL VARIABLE INITIATION
density = {'name':'density',
           'values':['low', 'medium', 'high']}
distribution = {'name':'distribution',
                'values':['even', 'uneven 2', 'uneven 3']}
void_size = {'name':'void_size',
             'values':[10, 17.5, 25]}
void_number = {'name':'void_number',
               'values':[0, 4, 8]}
beta = {'name':'beta',
        'values':[0.2, 0.5, 1]}
same_plant_utility_func_exponent = {'name':'same_plant_utility_func_exponent',
                    'values':[-8, -5, 0]}
pairs_utility_func_exponent = {'name':'pairs_utility_func_exponent',
                    'values':[-8, -5, 0]}
symmetry = {'name':'symmetry',
             'values':['left-right', 'left-right-up-down', 'neither']}

# LIST OF ALL VARIABLES
all_variables = [density, distribution, void_size, void_number, beta, same_plant_utility_func_exponent,
                 pairs_utility_func_exponent, symmetry]

# DICT OF QUERIES
queries = {}
for x in range(42):
    queries[x] = {100 + x:{}, 200 + x:{}} # todo hard coded
print(queries)
# GENERAL VARIABLE ADDER FUNCTION: assumes queries is length 42, variable has 3 values. # todo hard coded
def add_variable(queries, variable):
    combos = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2]]
    indices = [x for x in range(42)] # todo hard coded
    for combo in combos:
        s = random.sample(indices, 7) # todo hard coded
        for i in s:
            indices.remove(i) # todo in progress
            queries[i]['left'][variable['name']] = variable['values'][combo[0]]
            queries[i]['right'][variable['name']] = variable['values'][combo[1]]
    return queries

# ADDING VARIABLES TO QUERIES
for variable in all_variables:
    queries = add_variable(queries, variable)

# MAKING THE INPUT VARIABLES DICTIONARY
for query in queries:
    gardens = [query['left'], query['right']]
    for garden in gardens:
        d = {}
        if garden['density'] == 'low':
            d['num_plants'] = np.full(9, 10)
        elif garden['density'] == 'medium':
            d['num_plants'] = np.full(9, 16)
        elif garden['density'] == 'high':
            d['num_plants'] = np.full(9, 22)
        if garden['distribution'] == 'uneven 2':
            for i in range(1, len(d['num_plants'])):
                if i == 4 or i == 5:
                    d['num_plants'][i] += 6
                else:
                    d['num_plants'][i] -= 2
        elif garden['distribution'] == 'uneven 3':
            for i in range(1, len(d['num_plants'])):
                if i == 3 or i == 4 or i == 5:
                    d['num_plants'][i] += 5
                else:
                    d['num_plants'][i] -= 3
        d['num_plants'][0] = garden['void_number']
        d['void_size'] = garden['void_size']
        d['beta'] = garden['beta']
        if garden['pairs_utility_func_exponent'] == 0:
            d['planting_groups'] = [[0], [8], [7], [6], [5], [4], [3], [2], [1]]
        else:
            d['planting_groups'] = [[0], [8, 4], [7, 3], [6, 2], [5, 1]]
        def clustering_utility_func(p, plant_type, other_plant_type, added_points):
            cum_p_dist = 0
            cum_s_dist = 0
            for o in added_points[plant_type]:
                o_loc = o[0]
                cum_s_dist += math.dist(p, o_loc)
            for o in added_points[other_plant_type]:
                o_loc = o[0]
                cum_p_dist += math.dist(p, o_loc)
            if cum_p_dist + cum_s_dist == 0:
                return 1
            else:
                return cum_p_dist ** d['pairs_utility_func_exponent'] + cum_s_dist ** d['same_plant_utility_func_exponent']
        def nps(candidates, plant_type, added_points):
            planting_groups = d['planting_groups']
            other_plant_type = None
            for g in planting_groups:
                if plant_type in g:
                    gc = g.copy()
                    gc.remove(plant_type)
                    other_plant_type = gc[0]
            assert other_plant_type is not None
            return next_point_selector_with_utility_func(candidates, plant_type, added_points,
                                                         lambda p, plant_type, added_points:
                                                         clustering_utility_func(p, plant_type,
                                                                                 other_plant_type,
                                                                                 added_points))
        d['next_point_selector'] = nps
        d['symmetry'] = garden['symmetry']

        # EXTRA SET VARIABLES FOR d
        d['bmca'] = bmca_utils.default_bac()

        # PUT THE d DICT INTO THE QUERY DICT
        garden['d'] = d

for query in queries:
    for t in range(num_trials):
                        plotting_utils.generate_garden_scatter_and_area(d=d, image_id=image_id, num_images=num_images,
                                                                        cylinder_nt=cylinder_nt, data=None, void_beta=void_beta,
                                                                        generate_plotly=generate_plotly,
                                                                        save_plotly=save_plotly, save_2d=save_2d, trialno=t)
