import numpy as np
import random
import garden_constants
import math
from numpy.random import default_rng
rng = default_rng()


def flip(p):
    r = random.random()
    if r < p:
        return 1
    else:
        return 0


def random_round(x):
    return random.choice([math.ceil(x), math.floor(x)])


def weighted_round(x):
    fx = math.floor(x)
    p = x - fx
    return fx + flip(p)


def weighted_round_or_one(x):
    r = max(weighted_round(x), 1)
    return r


def generate_garden(dims, cellsize, a, beta, num_p_selector):
    added_points = []
    ndim = dims.size
    dims = (dims / cellsize).astype(int)

    def inhibition_radius(plant_type):
        return garden_constants.plant_radii[plant_type] / cellsize

    garden_area = np.prod(dims)
    est_area = a * garden_area
    frac_tot_area_p = np.full(garden_constants.num_plants, 1 / garden_constants.num_plants)
    est_tot_area_p = frac_tot_area_p * est_area
    area_p = [math.pi * (inhibition_radius(p) ** 2)
              for p in range(garden_constants.num_plants)]
    num_p = est_tot_area_p / area_p
    num_p = np.array([num_p_selector(n) for n in num_p], dtype=int)

    def next_point(plant_type):
        r = inhibition_radius(plant_type)
        crm = get_cr_map(points)
        cbm = get_cb_map(points)
        c1 = crm > ((1 - beta) * r)
        c2 = cbm > r
        c3 = dist_to_border >= r
        criteria = (c1 & c2 & c3)
        candidates = points[criteria]
        if len(candidates) == 0:
            return False
        choice = candidates[rng.integers(candidates.shape[0])]
        add_point(get_point_coords(choice), plant_type)
        return True

    def add_point(choice, plant_type):
        xc, yc = choice
        rc = inhibition_radius(plant_type)
        pl = get_point_list(points)
        for m in pl:
            mx, my = get_point_coords(m)
            d = math.dist([xc, yc], [mx, my])
            dr = max(d - rc, 0)
            db = max(d - ((1 - beta) * rc), 0)
            if dr < get_cr(m):
                set_cr(mx, my, dr)
            if db < get_cb(m):
                set_cb(mx, my, db)
        mark_plant(xc, yc, plant_type)
        added_points.append(choice)

    # points stores point locations:
    # points[x, y] = [x, y, cr, cb, t]
    # b = 1.0 if plant here, 2.0 if point is blocked, np.nan if no plant.
    # x, y is loc of plant
    # cp is distanct to closest plant
    # t is type of plant, as plant index
    points = np.full(np.append(dims, ndim + 3), np.nan, dtype=np.float32)
    it = np.nditer(points, flags=["multi_index", "refs_ok"])
    for _ in it:
        if it.multi_index[2] == 0:
            points[it.multi_index] = it.multi_index[0]
        elif it.multi_index[2] == 1:
            points[it.multi_index] = it.multi_index[1]
        elif it.multi_index[2] == 2 or it.multi_index[2] == 3:
            points[it.multi_index] = np.inf

    def get_point_coords(p):
        return p[0:2]

    def get_cr(p):
        return p[2]

    def get_cb(p):
        return p[3]

    def get_plant_type(p):
        return p[4]

    def set_cr(x, y, cr):
        points[int(x), int(y), 2] = cr

    def set_cb(x, y, cb):
        points[int(x), int(y), 3] = cb

    def mark_plant(x, y, t):
        points[int(x), int(y), 4] = t

    def get_cr_map(pointsx):
        return pointsx[:, :, 2]

    def get_cb_map(pointsx):
        return pointsx[:, :, 3]

    def get_point_list(pointsx):
        return pointsx.reshape(pointsx.shape[0] * pointsx.shape[1], pointsx.shape[2])

    def get_plant_list(pointsx):
        pointlist = get_point_list(pointsx)
        return pointlist[np.array([(not np.isnan(p[4])) for p in pointlist])]

    dist_to_border = np.empty(dims)
    it = np.nditer(dist_to_border, flags=["multi_index", "refs_ok"])
    for _ in it:
        xp, yp = it.multi_index
        dimx, dimy = dims
        dtbs_list = [xp, dimx - xp, yp, dimy - yp]
        dist_to_border[it.multi_index] = min(dtbs_list)

    plant_index = garden_constants.num_plants - 1

    master_break = False
    while plant_index >= 0 and not master_break:
        if plant_index > 0:
            for _ in range(num_p[plant_index]):
                n = next_point(plant_index)
                if not n:
                    break
            plant_index -= 1
        else:
            while True:
                n = next_point(plant_index)
                if not n:
                    master_break = True
                    break

    # to cartesian
    final_points = get_plant_list(points)
    return np.array([np.array([get_point_coords(x) * cellsize, get_plant_type(x)], dtype=object)
                     for x in final_points])

    # Util functions
    def bounded_cluster(shape, radius):
        if shape == 'circle':
            def in_bounds(p):
               loc, plant_index, r = point_unpacker(p)

    def line_following(function, input_range):
        pass

    def shift_sample(data, x_shift, y_shift):
        pass

    def rotate_sample(data, theta):
        pass

def cart_to_polar(x, y):
    return math.sqrt(x ** 2 + y ** 2), math.tan(y / x)

def point_unpacker(p):
    loc, plant_index = p
    plant_index = int(plant_index)
    r = garden_constants.plant_radii[plant_index]
    return loc, plant_index, r
