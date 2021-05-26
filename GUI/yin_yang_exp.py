import garden_constants
import poisson_disk.poisson_disc as poi
import plotting_utils

def u(x):
    return x + 10


def l(x):
    return 0


bounds = [0, 10]
num_checks = 10
"""

def generate_garden_scatter_and_area(a, beta, num_p_selector, bounds_map_creator_args, 
                                     show=False, save=False):
                                     
"""
plotting_utils.generate_garden_scatter_and_area(beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[u, l, bounds, num_checks], show=True, save=True)

