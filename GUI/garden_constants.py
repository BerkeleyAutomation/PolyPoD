import numpy as np


garden_x_len = 20
garden_y_len = 20
plant_max_radius = 1.5
plant_min_radius = 0.5
garden_dimensions = (garden_x_len, garden_y_len, plant_max_radius)
dims = np.array([garden_x_len, garden_y_len])
garden_area = np.prod(dims)
cellsize = 0.2
a_func_multiplier = 0.328
a_func_offset = 0.663
a_func_exp_base = 3.71

colors_of_plants = ["#7e8c3e", "#5c702f", "#92966c", "#343f33", "#919b3e", "#557554", "#b2cbb2", "#6e7d68",
                    "#7fae7e", "#455127", '#32C822']
colors_of_plants_hi_contrast = ['black', 'brown', 'darkviolet', 'blue', 'darkgreen', 'lime',
                                'gold', 'orange', 'fuchsia', 'red']

colors_of_plants_shibui = ['#00af42', '#00a265', '#00B146',
                           '#068b2e', '#00601D', '#2Ab500',
                           '#13b510', '#006806', '#11A011',
                           '#10b060']

colors_of_plants_hcl_v2 = ["#004800", "#005100", "#005A00",
                           "#006300", "#026D00", "#107600",
                           "#1C7F00", "#278900", "#33921E",
                           "#3E9B1F"]
soil_color = "#50371f"
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