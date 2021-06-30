import numpy as np
import math
from matplotlib.lines import Line2D

garden_x_len = 150
garden_y_len = 150
plant_max_radius = 5 # unused
plant_min_radius = 3 # unused
garden_dimensions = (garden_x_len, garden_y_len, plant_max_radius)
dims = np.array([garden_x_len, garden_y_len])
garden_area = np.prod(dims)
cellsize = 1
assert plant_min_radius / cellsize >= 2
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
'''
plant_radii = {
 'swiss_chard': 27, #31
 'kale': 35, #35
 'green_lettuce': 16, #(18,1)
 'cilantro': 12,
 'red_lettuce': 13,#15
 'borage': 29, #(60,5) 
 'sorrel': 9,
 'radicchio': 24,#29
 'arugula': 21, #(25,1)
 'turnip': 31 #33
}
'''
plant_radii = {
9:35, # kale
8:31, # turnip
7:29, # borage
6:27, # swiss_chard
5:24, # radicchio
4:21, # arugula
3:16, # green_lettuce
2:13, # red_lettuce
1:12, # cilantro
0:9   # sorrel
}

plantid2name = {
9:'kale', # red
8:'turnip', # fuchsia
7:'borage', # orange
6:'swiss_chard', # gold
5:'radicchio', # lime
4:'arugula', # darkgreen
3:'green_lettuce', # blue
2:'red_lettuce', # darkviolet
1:'cilantro', # brown
0:'sorrel' # black
}
SRV = -1.0
PLANTS_RELATION = {
        "borage":       {"borage": SRV, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 1.0, "arugula": 0.0, "swiss_chard": 1.0, "turnip": 0.0},
        "sorrel":       {"borage": 0.0, "sorrel": SRV,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "cilantro":     {"borage": -1.0, "sorrel": 0.0,  "cilantro": SRV, "radicchio": 0.0, "kale": -1.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "radicchio":    {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": SRV, "kale": 0.0, "green_lettuce":-1.0, "red_lettuce":-1.0, "arugula": 0.0, "swiss_chard":-1.0, "turnip": 0.0},
        "kale":         {"borage": -1.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 1.0, "kale": SRV, "green_lettuce": -1.0, "red_lettuce": -1.0, "arugula": -1.0, "swiss_chard": 0.0, "turnip": 0.0},
        "green_lettuce":{"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": SRV, "red_lettuce": -1.0, "arugula": 0.0, "swiss_chard": -1.0, "turnip": 0.0},
        "red_lettuce":  {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": -1.0, "kale": -1.0, "green_lettuce": -1.0, "red_lettuce": SRV, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "arugula":      {"borage": 0.0, "sorrel": 1.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 1.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": SRV, "swiss_chard": 0.0, "turnip": -1.0},
        "swiss_chard":  {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": SRV, "turnip": 0.0},
        "turnip":       {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": -1.0, "swiss_chard": 1.0, "turnip": SRV}
}
plantid2name = {
9:'kale', # red
8:'turnip', # fuchsia
7:'borage', # orange
6:'swiss_chard', # gold
5:'radicchio', # lime
4:'arugula', # darkgreen
3:'green_lettuce', # blue
2:'red_lettuce', # darkviolet
1:'cilantro', # brown
0:'sorrel' # black
}
legend_elements = [Line2D([0], [0], marker='o', color='k', label='kale',
                          markerfacecolor='red', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='turnip',
                          markerfacecolor='fuchsia', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='borage',
                          markerfacecolor='orange', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='swiss chard',
                          markerfacecolor='gold', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='radicchio',
                          markerfacecolor='lime', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='arugula',
                          markerfacecolor='darkgreen', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='green lettuce',
                          markerfacecolor='blue', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='red lettuce',
                          markerfacecolor='darkviolet', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='cilantro',
                          markerfacecolor='brown', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='sorrel',
                          markerfacecolor='black', markersize=12)
                   ]

# added points is list of ten lists, one for each plant type!
def point_companionship_score(p, plant_type, added_points, self_multiplier=1):
    cum_comp = 0
    p_name = plantid2name[plant_type]
    for t in range(num_plants):
        t_name = plantid2name[t]
        c = PLANTS_RELATION[p_name][t_name]
        t_comp = 0
        if not c == 0:
            for o in added_points[t]:
                o_loc = o[0]
                if math.dist(p, o_loc) > 0:
                    p_o_score = (c / ((math.dist(p, o_loc)) ** 2))
                    if plant_type == t:
                        t_comp += p_o_score * self_multiplier
                    else:
                        t_comp += p_o_score
            cum_comp += t_comp
    return cum_comp

def garden_companionship_score(added_points):
    garden_comp = 0
    temp = [[] for _ in range(10)]
    for p in added_points:
        loc, t = p
        temp[int(t)].append(p)
    added_points = temp
    #print('added points\n', added_points)
    for type_list in added_points:
            for point in type_list:
                loc, t = point
                garden_comp += point_companionship_score(loc, t, added_points)
    return garden_comp * 10000 # cm to m

def comp_pd_postprocessing(pd, exp):
    '''
    probs = [p[1] for p in pd]
    postprocessed_probs = exp ** (probs - np.min(probs)) - 1
    points = [p[0] for p in pd]
    return np.array(list(zip(points, postprocessed_probs)))
    '''
    return exp ** (pd - np.min(pd)) - 1
def point_unpacker(p):
    loc, plant_index = p
    plant_index = int(plant_index)
    r = plant_radii[plant_index]
    return loc, plant_index, r