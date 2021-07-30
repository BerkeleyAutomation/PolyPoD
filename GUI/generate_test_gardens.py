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
import copy

# GENERAL VARIABLES: SET
num_trials = 1
num_p_selector = poi.weighted_round_or_one
data = None
cylinder_nt = 70
generate_plotly=True
save_plotly=True
save_2d=True
void_beta = -6
def random_ps(candidates, plant_type, added_points, planting_groups):
    draw = candidates[rng.integers(len(candidates))]
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

# EXPERIMENTAL VARIABLE DEFAULT VALUES: DO NOT CHANGE
density = {'name':'density',
           'values':['medium', 'low', 'high']}
distribution = {'name':'distribution',
                'values':['even', 'uneven 2', 'uneven 3']}
void_size = {'name':'void_size',
             'values':[17.5, 10, 25]}
void_number = {'name':'void_number',
               'values':[0, 4, 8]}
beta = {'name':'beta',
        'values':[0.6, 0.2, 0.4, 0.8, 1]}
same_plant_utility_func_exponent = {'name':'same_plant_utility_func_exponent',
                    'values':[0, -6, -12, -100]}
pairs_utility_func_exponent = {'name':'pairs_utility_func_exponent',
                    'values':[0, -6, -12, -100]}
symmetry = {'name':'symmetry',
             'values':['neither', 'left-right', 'left-right-up-down']}

# EXPERIMENTAL VARIABLE EXPERIMENTAL VARIABLES: CAN CHANGE
num_trials = 1
density = {'name':'density',
           'values':['low']}
distribution = {'name':'distribution',
                'values':['uneven 2']}
void_size = {'name':'void_size',
             'values':[0]}
void_number = {'name':'void_number',
               'values':[0]}
beta = {'name':'beta',
        'values':[0.2]}
same_plant_utility_func_exponent = {'name':'same_plant_utility_func_exponent',
                    'values':[0]}
pairs_utility_func_exponent = {'name':'pairs_utility_func_exponent',
                    'values':[0]}
symmetry = {'name':'symmetry',
             'values':['neither']}

# LIST OF ALL VARIABLES
all_variables = [density, distribution, void_size, void_number, beta, same_plant_utility_func_exponent,
                 pairs_utility_func_exponent, symmetry]

combos = [{}]
def variable_adder(l, variable):
    nl = []
    for d in l:
        for val in variable['values']:
            d = d.copy()
            d[variable['name']] = val
            nl.append(d)
    return nl
for var in all_variables:
    combos = variable_adder(combos, var)
# DICT OF QUERIES
queries = {}
for x in range(42):
    queries[x] = {100 + x:{}, 200 + x:{}} # todo hard coded
#print(queries)
# GENERAL VARIABLE ADDER FUNCTION: assumes queries is length 42, variable has 3 values. # todo hard coded

'''
# INDEPENDENT TESTING OF THE VARIABLE
independent = []
default_dictionary = {}
for other in all_variables:
    default_dictionary[other['name']] = other['values'][0]
#independent.append(default_dictionary)
def debugging_amend(d):
    d['beta'] = 1
    d['density'] = 'high'
def independent_add_variable(l, variable):
    d = {}
    for other in all_variables:
        d[other['name']] = other['values'][0]
    d[variable['name']] = variable['values'][1]
    debugging_amend(d)
    l.append(d)
    dc = d.copy()
    dc[variable['name']] = variable['values'][2]
    debugging_amend(dc)
    l.append(dc)
    return l

ADDING VARIABLES TO INDEPENDANT
for variable in [symmetry]:
    independent = independent_add_variable(independent, variable)

for c, i in enumerate(independent):
    print(c)
    for v in i:
        print(f'\t{v} {i[v]}')

# ADDING VARIABLES TO QUERIES
for variable in all_variables:
    queries = add_variable(queries, variable)
'''
# MAKING THE INPUT VARIABLES DICTIONARY
def add_d_to_queries(queries):
    for query in queries:
        gardens = [query['left'], query['right']]
        for garden in gardens:
            add_d_to_garden(garden)

def add_d_to_garden(garden):
    d = {}

    # EXTRA SET VARIABLES FOR d
    d['bmca'] = [bmca_utils.default_bac()]

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
        d['bmca'][0][4] = [[0], [8], [7], [6], [5], [4], [3], [2], [1]] # planting groups
    else:
        d['bmca'][0][4] = [[0], [8, 4], [7, 3], [6, 2], [5, 1]] # Planting groups

    def clustering_utility_func(p, plant_type, other_plant_type, added_points):
        if plant_type == other_plant_type:
            exp = garden['same_plant_utility_func_exponent']
        else:
            exp = garden['pairs_utility_func_exponent']
        cum_dist = 0
        for o in added_points[other_plant_type]:
            o_loc = o[0]
            cum_dist += math.dist(p, o_loc)
        if cum_dist + cum_dist == 0:
            return 1
        else:
            return cum_dist ** exp

    def nps(candidates, plant_type, added_points, planting_groups):
        if plant_type == 0:
            return random_ps(candidates, plant_type, added_points, planting_groups)
        else:
            other_plant_type = None
            for g in planting_groups:
                if plant_type in g:
                    if len(g) > 1:
                        gc = g.copy()
                        gc.remove(plant_type)
                        other_plant_type = gc[0]
                    else:
                        other_plant_type = plant_type
            assert other_plant_type is not None
            utility_func = lambda p, plant_type, added_points: clustering_utility_func(p, plant_type,
                                    other_plant_type,
                                    added_points)
        return next_point_selector_with_utility_func(candidates, plant_type, added_points, utility_func)

    d['next_point_selector'] = nps
    d['symmetry'] = garden['symmetry']


    # PUT THE d DICT INTO THE QUERY DICT
    garden['d'] = d
    return garden

for garden in combos:
    add_d_to_garden(garden)

print(f'num images: {len(combos) * num_trials}')
for c, garden in enumerate(combos):
    for t in range(num_trials):
        next_garden = copy.deepcopy(garden)
        plotting_utils.generate_garden_scatter_and_area(d=next_garden['d'], image_id=c * num_trials + t, num_images=len(combos) * num_trials,
                                                        cylinder_nt=cylinder_nt, data=None, void_beta=void_beta,
                                                        generate_plotly=generate_plotly,
                                                        save_plotly=save_plotly, save_2d=save_2d)
