import SeedPlacementGenerator
import numpy as np
from numpy.random import default_rng
rng = default_rng()


class RandomSeedPlacementGenerator(SeedPlacementGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__()
        assert (len(kwargs) == 1)
        assert ('prob_of_plant' in kwargs.keys())
        self.prob_of_plant = kwargs['prob_of_plant']

    def generate_seed_placement(self, *args, **kwargs):
        r = []
        for _ in range(2):
            plant_present = rng.binomial(1, self.prob_of_plant, [self.garden_x_len, self.garden_y_len])
            plant_matrix = np.zeros((self.garden_x_len, self.garden_y_len, self.num_plants), dtype='float')
            it = np.nditer(plant_present, flags=["multi_index"])
            for x in it:
                if x == 1:
                    plant_type = rng.integers(self.num_plants)
                    plant_matrix[it.multi_index[0], it.multi_index[1], plant_type] = \
                        self.plant_height(plant_type)
            r.append(SeedPlacementGenerator.SeedPlacementGenerator(plant_matrix))
        return r
