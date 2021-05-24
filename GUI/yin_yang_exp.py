import garden_constants
import poisson_disk.poisson_disc as poi
import a_beta_exp as abe

def u(x):
    return x + 10


def l(x):
    return 0


bounds = [0, 10]
num_checks = 10

data = poi.generate_garden(garden_constants.dims, garden_constants.cellsize,
                beta=0.5, a=0.95, num_p_selector=poi.weighted_round_or_one,
                bounds_map_creator_args=[u, l, bounds, num_checks])

