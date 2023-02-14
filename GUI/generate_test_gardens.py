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
#mode = 'random draw' # 'random draw' or 'combos'
mode = 'combos'
num_trials = 1
num_gardens_to_generate = 1
num_p_selector = poi.weighted_round_or_one
data = None
cylinder_nt = 70
generate_plotly=False
save_plotly=True
save_2d=False

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
           'values':[0.25, 0.5, 0.75, 1]}
distribution = {'name':'distribution',
                'values':['even', 'uneven 2', 'uneven 3']}
beta = {'name':'beta',
        'values':[0, 0.2, 0.4, 0.6, 0.8, 1]}
void_size = {'name':'void_size',
             'values':[15, 35, 50, 75, 100]}
void_number = {'name':'void_number',
               'values':[0, 2, 4, 8, 16]}
utility_func_exponent = {'name':'utility_func_exponent',
                    'values':[['same', 0], ['same', -6], ['same', -12], ['same', -100], ['pairs', -6], ['pairs', -12], ['pairs', -100]]}
symmetry = {'name':'symmetry',
             'values':['neither', 'left-right', 'left-right-up-down']}

# EXPERIMENTAL VARIABLE EXPERIMENTAL VARIABLES: CAN CHANGE
density = {'name':'density',
           'values':[0.5]}
distribution = {'name':'distribution',
                'values':['even']}
void_size = {'name':'void_size',
             'values':[35]}
void_number = {'name':'void_number',
               'values':[8]}
beta = {'name':'beta',
        'values':[1]}
utility_func_exponent = {'name':'utility_func_exponent',
                    'values':[['same', -6]]}
symmetry = {'name':'symmetry',
             'values':['neither']}

coordinates = {'name': 'coordinates',
               'values': [[[100, 100], [200, 100], [200, 200], [300, 200], [300, 100], [400, 100], [400, 400],[250, 250], [250, 400], [100, 400], [100, 300], [175, 250], [100, 200], [100, 100]]]
}
num_each_plant = {'name': 'num_each_plant',
               'values': np.full(9, 2)
}

# LIST OF ALL VARIABLES
all_variables = [density, distribution, void_size, void_number, beta, utility_func_exponent, symmetry, coordinates, num_each_plant]

if mode == 'combos':
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

elif mode == 'random draw':
    combos = []
    for n in range(num_gardens_to_generate):
        garden = {}
        for var in all_variables:
            garden[var['name']] = random.choice(var['values'])
        combos.append(garden)
else:
    raise ValueError('mode must be combos or random draw')
# ADD d TO GARDEN
def add_d_to_garden(garden):
    d = {}

    # EXTRA SET VARIABLES FOR d
    #d['bmca'] = [bmca_utils.default_bac()]
    coordinates = garden["coordinates"]
    num_each_plant = garden["num_each_plant"]
    
    d['bmca'] = [bmca_utils.bac_with_parameters(coordinates, num_each_plant)]

    # DEFAULT HI-DENSITY PLANT NUMS FOR EVEN DISTRIBUTION, NO VOIDS
    beta = garden['beta']
    default_num_plants = 9 if beta == 0 else 10 if beta == 0.2 else 12 if beta == 0.4 else 14 if beta == 0.6 else 17 if beta == 0.8 else 21
    small_plant_extra = 2

    d['num_plants'] = np.concatenate((np.full(4, default_num_plants + small_plant_extra), np.full(5, default_num_plants)))
    d['beta'] = garden['beta']

    # DISTRIBUTION ADJUSTMENT
    distribution_offset = 0.6
    if garden['distribution'] == 'uneven 2':
        for i in range(1, len(d['num_plants'])):
            if i == 4 or i == 5:
                d['num_plants'][i] = int(d['num_plants'][i] * 5/2)
            else:
                d['num_plants'][i] = int(d['num_plants'][i] * 3/4 * distribution_offset)
    elif garden['distribution'] == 'uneven 3':
        for i in range(1, len(d['num_plants'])):
            if i == 3 or i == 4 or i == 5:
                d['num_plants'][i] = int(d['num_plants'][i] * 9/4)
            else:
                d['num_plants'][i] = int(d['num_plants'][i] * 3/4 * distribution_offset)

    # VOID NUMBER AND SIZE
    d['num_plants'][0] = garden['void_number']
    vs = garden['void_size']
    d['void_beta'] = 0 # old stuff: -4 if vs == 15 else 0 if vs == 100 else -2

    d['void_size'] = garden['void_size']

    # DENSITY OFFSET
    d['num_plants'] = [int(x * garden['density']) for x in d['num_plants']]

    # CLUSTERING UTILTY FUNCS
    if garden['utility_func_exponent'][0] == 'same':
        d['bmca'][0][2] = [[0], [8], [7], [6], [5], [4], [3], [2], [1]] # planting groups
    else:
        d['bmca'][0][2] = [[0], [8, 4], [7, 3], [6, 2], [5, 1]] # Planting groups

    def clustering_utility_func(p, plant_type, other_plant_type, added_points, dims, d):
        exp = garden['utility_func_exponent'][1]
        cum_dist = 0
        for o in added_points[other_plant_type]:
            o_loc = o[0]
            if d['symmetry'] == 'left-right':
                if o_loc[0] > dims[1] / 2:
                    continue
            elif d['symmetry'] == 'left-right-up-down':
                if o_loc[0] > dims[1] / 2 or o_loc[1] > dims[0] / 2:
                    continue
            cum_dist += math.dist(p, o_loc)
        if cum_dist + cum_dist == 0:
            return 1
        else:
            return cum_dist ** exp

    def nps(candidates, plant_type, added_points, planting_groups, dims, d):
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
                                    added_points, dims, d)
        return next_point_selector_with_utility_func(candidates, plant_type, added_points, utility_func)
    d['next_point_selector'] = nps

    # SYMMETRY
    d['symmetry'] = garden['symmetry']

    # PUT THE d DICT INTO THE QUERY DICT
    garden['d'] = d
    
    return garden

for garden in combos:
    add_d_to_garden(garden)


# GENERATE
#num_images = len(combos) * num_trials
num_images = 1
print(f'num images: {num_images}')
for c, garden in enumerate(combos):
    for t in range(num_trials):
        next_garden = copy.deepcopy(garden)
        plotting_utils.generate_garden_scatter_and_area(d=next_garden['d'], image_id=c * num_trials + t, num_images=num_images,
                                                        cylinder_nt=cylinder_nt, data=None,
                                                        generate_plotly=generate_plotly, garden=next_garden,
                                                        save_plotly=save_plotly, save_2d=save_2d)
