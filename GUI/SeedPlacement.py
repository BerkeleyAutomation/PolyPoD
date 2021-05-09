import numpy as np
import garden_constants


class SeedPlacement:
    def __init__(self, plant_matrix=None):
        self.seed_placement = plant_matrix

    def set_seed_placement(self, plant_matrix):
        self.seed_placement = plant_matrix
    # Return random plant radius: for now, just 0.5, but later we can sample from a distribution
    # or something.
    def plant_radius(self, plant_type, plant_height):
        return plant_height

    def plant_height(self, plant_type):
        return garden_constants.plant_height_distribution_params[plant_type]

    # Returns plant x, y, z, and radius from an iterator over the plant seed placement matrix
    # with multi-index, and the value returned by the iterator.
    def get_plant_data(self, it, p):
        plant_type = it.multi_index[2]
        return it.multi_index[0], it.multi_index[1], p, self.plant_radius(plant_type, p)

    # Return color of plant
    def get_plant_color(self, it):
        return garden_constants.colors_of_plants[it.multi_index[2]]

    def plant_present(self, p):
        return not (p == 0)
