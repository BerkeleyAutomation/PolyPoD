import numpy as np


garden_x_len = 20
garden_y_len = 20
plant_max_radius = 1.5
plant_min_radius = 0.5
garden_dimensions = (garden_x_len, garden_y_len, plant_max_radius)
dims = np.array([garden_x_len, garden_y_len])
garden_area = np.prod(dims)
cellsize=2
colors_of_plants = ["#7e8c3e", "#5c702f", "#92966c", "#343f33", "#919b3e", "#557554", "#b2cbb2", "#6e7d68",
                    "#7fae7e", "#455127"]
colors_of_plants_hi_contrast = ['black', 'brown', 'darkviolet', 'blue', 'darkgreen', 'lime',
                                'gold', 'orange', 'fuchsia', 'red']
soil_color = "#7c5e42"
num_plants = 10
alpha = 1
plant_radii = {}
for p, r in enumerate(np.linspace(plant_min_radius, plant_max_radius, num_plants)):
    plant_radii[p] = r

def point_unpacker(p):
    loc, plant_index = p
    plant_index = int(plant_index)
    r = plant_radii[plant_index]
    return loc, plant_index, r