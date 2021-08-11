import numpy as np
import math
from matplotlib.lines import Line2D

garden_x_len = 450
garden_y_len = 450
dims = np.array([garden_x_len, garden_y_len])
garden_area = np.prod(dims)
cellsize = 3
a_func_multiplier = 0.328
a_func_offset = 0.663
a_func_exp_base = 3.71
average_other_radii = 23.275
void_radius = 5
void_dist_to_border = 0
def reverse(a):
    ar = a[1:][::-1]
    ar.insert(0, a[0])
    return ar

colors_of_plants = ["#7e8c3e", "#5c702f", "#92966c", "#343f33", "#919b3e", "#557554", "#b2cbb2", "#6e7d68",
                    "#7fae7e", "#455127", '#32C822']
colors_of_plants_hi_contrast = ['black', 'darkviolet', 'blue', 'darkgreen', 'lime',
                                'gold', 'orange', 'fuchsia', 'red']

colors_of_plants_shibui = ['#00af42', '#00a265', '#00B146',
                           '#068b2e', '#00601D', '#2Ab500',
                           '#13b510', '#006806', '#11A011',
                           '#10b060']

colors_of_plants_hcl_v2 = ["#004800", "#005100", "#005A00",
                           "#006300", "#026D00", "#107600",
                           "#1C7F00", "#278900", "#33921E",
                           "#3E9B1F"]

color_atsu_orig_ordering =  ['#000000', "#6E8236", "#8CAB6D",
                             "#6DA54C", "#4B8A41","#5C996C",
                             "#538B82", "#537960", "#516758"]

color_atsu_my_edit = ['#000000', "#8CAB6D", "#6DA54C", # cut 8 and 10
                      "#4D9932", "#4B8A41","#5C996C",
                      "#538B82", "#537960", "#40785B"]

color_atsu_my_edit_reverse = color_atsu_my_edit[1:][::-1]
color_atsu_my_edit_reverse.insert(0, color_atsu_my_edit[0])

color_custom_order_ignore = ['#000000', '#5C996C', '#40785B',
                      '#4D9932', '#8CAB6D','#6DA54C',
                      '#537960', '#538B82', '#4B8A41']

color_v1_custom_order   = ['#000000', '#5C996C', "#6E8236",
                        "#516758", '#8CAB6D','#6DA54C',
                        '#537960', '#538B82', '#4B8A41']
                      # 0       1       2       3       4       5       6       7       8
                       #000000, #6E8236,#8CAB6D,#6DA54C,#4B8A41,#5C996C,#538B82,#537960,#516758]
color_custom_mix_rearrange = [0, 5, 1, 8, 2, 3, 7, 6, 4]
saturation_5 = ['#000000', '#6F8433','#8CAF69','#6BA848','#498E3E','#579E6A','#509086','#4E7E5F','#4D6B56']
brightness_5 = ['#000000', '#778D3B','#92AF75','#72AD50','#519546','#62A172','#5A958B','#598267','#587060']
saturation_brightness_5 = ['#000000', '#789038','#92B371','#71B14C','#4E9843','#5CA670','#559A90','#538866','#54745E']
saturation_10 = ['#000000', '#708731','#8CB465','#6AAC44','#46913B','#53A268','#4C9589','#4A825E','#496F55']
brightness_10 = ['#000000', '#819840','#98B47C','#79B258','#56A04B','#6AA57A','#5F9E94','#5F8C6F','#5F7967']
saturation_brightness_10 = ['#000000', '#849F39','#98BB75','#77BA51','#51A744','#61AE76','#56A799','#56956C','#558364']
saturation_5_brightness_10 = ['#000000', '#829C3D','#98B779','#78B655','#54A348','#65AA78','#5AA398','#59916D','#5B7D65']
saturation_10_brightness_5 = ['#000000', '#7A9335','#92B76D','#70B548','#4C9C40','#59A96E','#519E91','#508B65','#4F795C']
greens_palette = ['#000000', '#C8E7AB','#ABCE8D','#8CB370','#77B353','#7C9C1F','#629364','#486233','#254514']

abandoned_colors = ['#073300', '094400', '#0a5200']
'''
color_atsu_orig_ordering.remove("#8CAB6D")
color_atsu_orig_ordering.remove("#6DA54C")
color_atsu_orig_ordering = color_atsu_orig_ordering[::-1]
'''
soil_color_atsu = "#2C1F16"
#soil_color = "#50371f"
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
8:35, # kale
7:31, # turnip
6:29, # borage
5:27, # swiss_chard
4:24, # radicchio
3:16, # green_lettuce
2:13, # red_lettuce
1:12, # cilantro
0: -1, # VOID: Variable radius!
}

num_plants = len(plant_radii)
plantid2name = {
8:'kale', # red
7:'turnip', # fuchsia
6:'borage', # orange
5:'swiss_chard', # gold
4:'radicchio', # lime
3:'green_lettuce', # darkgreen
2:'red_lettuce', # blue
1:'cilantro', # darkviolet
0: 'VOID' # black
}

SRV = -1.0
PLANTS_RELATION = {
        "borage":       {"borage": SRV, "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 1.0, "swiss_chard": 1.0, "turnip": 0.0, "VOID": 0.0},
        "cilantro":     {"borage": -1.0, "cilantro": SRV, "radicchio": 0.0, "kale": -1.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "swiss_chard": 0.0, "turnip": 0.0, "VOID": 0.0},
        "radicchio":    {"borage": 0.0, "cilantro": 0.0, "radicchio": SRV, "kale": 0.0, "green_lettuce":-1.0, "red_lettuce":-1.0, "swiss_chard":-1.0, "turnip": 0.0, "VOID": 0.0},
        "kale":         {"borage": -1.0, "cilantro": 0.0, "radicchio": 1.0, "kale": SRV, "green_lettuce": -1.0, "red_lettuce": -1.0, "swiss_chard": 0.0, "turnip": 0.0, "VOID": 0.0},
        "green_lettuce":{"borage": 0.0, "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": SRV, "red_lettuce": -1.0, "swiss_chard": -1.0, "turnip": 0.0, "VOID": 0.0},
        "red_lettuce":  {"borage": 0.0, "cilantro": 0.0, "radicchio": -1.0, "kale": -1.0, "green_lettuce": -1.0, "red_lettuce": SRV, "swiss_chard": 0.0, "turnip": 0.0, "VOID": 0.0},
        "swiss_chard":  {"borage": 0.0, "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "swiss_chard": SRV, "turnip": 0.0, "VOID": 0.0},
        "turnip":       {"borage": 0.0, "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "swiss_chard": 1.0, "turnip": SRV, "VOID": 0.0},
        "VOID":         {"borage": 0.0, "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "swiss_chard": 0.0, "turnip": 0.0, "VOID": 0.0},
}

legend_elements = [Line2D([0], [0], marker='o', color='k', label='8 kale',
                          markerfacecolor='red', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='7 turnip',
                          markerfacecolor='fuchsia', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='6 borage',
                          markerfacecolor='orange', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='5 swiss chard',
                          markerfacecolor='gold', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='4 radicchio',
                          markerfacecolor='lime', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='3 green lettuce',
                          markerfacecolor='darkgreen', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='2 red lettuce',
                          markerfacecolor='blue', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='1 cilantro',
                          markerfacecolor='darkviolet', markersize=12),
                   Line2D([0], [0], marker='o', color='k', label='0 VOID',
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