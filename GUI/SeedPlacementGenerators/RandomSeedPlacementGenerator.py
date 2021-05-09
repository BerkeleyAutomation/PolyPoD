from SeedPlacementGenerators import SeedPlacementGenerator
import SeedPlacement
import numpy as np
from numpy.random import default_rng
rng = default_rng()
import garden_constants
import argparse


class RandomSeedPlacementGenerator(SeedPlacementGenerator.SeedPlacementGenerator):
    default_prob_of_plant = 0.05
    def __init__(self, **kwargs):
        super().__init__()
        if 'prob_of_plant' in kwargs.keys():
            self.prob_of_plant = kwargs['prob_of_plant']
        else:
            self.prob_of_plant = self.default_prob_of_plant

    def generate_seed_placement(self):
        sp = SeedPlacement.SeedPlacement()
        plant_present = rng.binomial(1, self.prob_of_plant, [garden_constants.garden_x_len,
                                                             garden_constants.garden_y_len])
        plant_matrix = np.zeros((garden_constants.garden_x_len, garden_constants.garden_y_len,
                                 garden_constants.num_plants), dtype='float')
        it = np.nditer(plant_present, flags=["multi_index"])
        for x in it:
            if x == 1:
                plant_type = rng.integers(garden_constants.num_plants)
                plant_matrix[it.multi_index[0], it.multi_index[1], plant_type] = \
                    sp.plant_height(plant_type)
        sp.set_seed_placement(plant_matrix)
        return sp
