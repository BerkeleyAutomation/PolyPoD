import numpy as np


class SeedPlacement:
    garden_x_len = 10
    garden_y_len = 10
    plant_max_height = 2
    plant_min_height = 0.5
    garden_dimensions = (garden_x_len, garden_y_len, plant_max_height)
    colors_of_plants = ["#7e8c3e", "#5c702f", "#92966c", "#343f33", "#919b3e", "#557554", "#b2cbb2", "#6e7d68",
                        "#7fae7e", "#455127"]
    num_plants = 10
    alpha = 1
    plant_height_distribution_params = {}
    for p, r in enumerate(np.linspace(plant_min_height, plant_max_height, num_plants)):
        plant_height_distribution_params[p] = r

    def __init__(self, plant_matrix):
        self.seed_placement = plant_matrix

    # Return random plant radius: for now, just 0.5, but later we can sample from a distribution
    # or something.
    def plant_radius(self, plant_type, plant_height):
        return plant_height

    def plant_height(self, plant_type):
        return self.plant_height_distribution_params[plant_type]

    # Returns plant x, y, z, and radius from an iterator with multi-index, and the value returned by
    # the iterator.
    def get_plant_data(self, it, p):
        plant_type = it.multi_index[2]
        return it.multi_index[0], it.multi_index[1], p, self.plant_radius(plant_type, p)

    # Return color of plant
    def get_plant_color(self, it):
        return self.colors_of_plants[it.multi_index[2]]

    def plant_present(self, p):
        return not (p == 0)
