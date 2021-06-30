import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi
import garden_constants
import math
import numpy as np

beta = 1
num_trials = 10
num_p_selector = poi.weighted_round_or_one
fill_final = True
data = None #np.load('french_plots/data_06-08-21_19-18-07-814772.npy', allow_pickle=True)
generate_plotly=False
save_plotly=False
save=True
# util_func = False
num_each_plant = np.full(10, 2, dtype='int')
#num_each_plant[9] = 2
comp_exps = [10 ** 8] #[2, 4, 8]
self_multipliers = [8] #[2, 4, 8]
from numpy.random import default_rng
from numpy.random import choice
rng = default_rng()

#bounds_map_creator_args = french_gardens_utils.french_demo_bac()
#bounds_map_creator_args = [[lambda x: 4, lambda x: 0, [0, 4, 0, 4]]]
bounds_map_creator_args = False

def random_ps(candidates, plant_type, added_points):
    draw = candidates[rng.integers(candidates.shape[0])]
    return [draw[0], draw[1]]
def next_point_selector(added_points):
    pass
for t in range(num_trials):
    plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                    data=data, generate_plotly=generate_plotly,
                                                    next_point_selector=random_ps,
                                                    save_plotly=save_plotly, save=save,
                                                    num_each_plant=num_each_plant, trialno=t)
