import garden_constants
import poisson_disk.poisson_disc as poi
import plotting_utils
import math

def u(x):
    return x + 10


def l(x):
    return 0


def u_diamond(x):
    if x <= 10:
        return x + 10
    else:
        return -x + 30


def l_diamond(x):
    if x <= 10:
        return -x + 10
    else:
        return x - 10


def u_silly(x):
    if x <= 2.661 or x >= 6.046:
        return math.sqrt(math.fabs(100 - (x - 10) ** 2)) + 10
    else:
        return (x - 4) ** 2 + 15


def l_silly(x):
    if x <= 13 or x >= 16:
        return 3 * math.sin(math.pi * x / 7) + 4
    else:
        return 0

bounds = [0, 10]
bounds_diamond = [0, 20]
num_checks = 10
"""

def generate_garden_scatter_and_area(a, beta, num_p_selector, bounds_map_creator_args, 
                                     show=False, save=False):
                                     
"""
plotting_utils.generate_garden_scatter_and_area(beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[[u_silly, l_silly, bounds_diamond, num_checks]], show=True, save=True)
