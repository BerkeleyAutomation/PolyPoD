import numpy as np
import random
import garden_constants
import math
from numpy.random import default_rng
rng = default_rng()
import time

def coin_flip(p):
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
    return fx + coin_flip(p)

def weighted_round_or_one(x):
    r = max(weighted_round(x), 1)
    return r

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

global_time_elapsed = 0
def generate_garden(dims, cellsize, beta, num_p_selector, bounds_map_creator_args, fill_final):
    # Preprocessing / Setup
    start = time.time()
    added_points = []
    ndim = dims.size
    dims = (dims / cellsize).astype(int)

    dist_to_border = np.empty(dims)
    it = np.nditer(dist_to_border, flags=["multi_index", "refs_ok"])
    for _ in it:
        xp, yp = it.multi_index
        dimx, dimy = dims
        dtbs_list = [xp, dimx - xp, yp, dimy - yp]
        dist_to_border[it.multi_index] = min(dtbs_list)

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

    def inhibition_radius(plant_type):
        return garden_constants.plant_radii[plant_type] / cellsize

    def point_unpacker_internal(p):
        loc, plant_index = p
        plant_index = int(plant_index)
        r = inhibition_radius(plant_index)
        return loc, plant_index, r

    # Main Helper Function
    def generate_garden_cluster(beta, bmca, starting_plants, points):
        if not bmca == False:
            upper, lower, bounds = bmca
            upper = memoize(upper)
            lower = memoize(lower)
            upper_grid = lambda a: (1 / cellsize) * upper(cellsize * a)
            lower_grid = lambda a: (1 / cellsize) * lower(cellsize * a)
            bounds = [num / cellsize for num in bounds]
            low_x_bound, high_x_bound, low_y_bound, high_y_bound = bounds

        def a_func(beta_arg):
            o = garden_constants.a_func_offset
            m = garden_constants.a_func_multiplier
            b = garden_constants.a_func_exp_base
            return (o - m) + m * (b ** beta_arg)

        a = a_func(beta)

        garden_area = np.prod(dims)
        est_area = a * garden_area
        frac_tot_area_p = np.full(garden_constants.num_plants, 1 / garden_constants.num_plants)
        est_tot_area_p = frac_tot_area_p * est_area
        area_p = [math.pi * (inhibition_radius(p) ** 2)
                  for p in range(garden_constants.num_plants)]
        num_p = est_tot_area_p / area_p
        num_p = np.array([num_p_selector(n) for n in num_p], dtype=int)

        # custom bounds functions
        def line_following(function, input_range):
            pass

        def bounds_map_creator(upper, lower, plant_type):
            def in_bounds(p):
                loc, plant_index, r = point_unpacker_internal(p)
                px = loc[0]
                py = loc[1]

                circ_up = ucv + py
                circ_low = lcv + py

                adjusted_cv = cvx + px
                upper_at_cv = np.array([upper(i) for i in adjusted_cv])
                lower_at_cv = np.array([lower(i) for i in adjusted_cv])

                upper_diff = upper_at_cv - circ_up
                if np.amin(upper_diff) < 0:
                    return False
                lower_diff = circ_low - lower_at_cv
                if np.amin(lower_diff) < 0:
                    return False
                in_left_right_bounds = (px - r) > low_x_bound and (px + r) < high_x_bound
                if not in_left_right_bounds:
                    return False
                return True

            bounds_map = np.full(dims, 0, dtype=bool)
            for x in range(math.ceil(low_x_bound), math.floor(high_x_bound)):
                for y in range(math.ceil(low_y_bound), math.floor(high_y_bound)):
                    bounds_map[x, y] = in_bounds([[x, y], plant_type])
            return bounds_map

        def standard_criteria(plant_type):
            r = inhibition_radius(plant_type)
            crm = get_cr_map(points)
            cbm = get_cb_map(points)
            c1 = crm > ((1 - beta) * r)
            c2 = cbm > r
            c3 = dist_to_border >= r
            criteria = (c1 & c2 & c3)
            return criteria

        def next_point(plant_type):
            scm = standard_criteria(plant_type)
            if bmca == False:
                criteria = scm
            else:
                bounds_map = bounds_map_creator(upper_grid, lower_grid, plant_type)
                criteria = scm & bounds_map
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

        plant_index = garden_constants.num_plants - 1

        # Inner Control (Plant Adding) Loop
        master_break = False
        while plant_index >= 0 and not master_break:
            r = inhibition_radius(plant_index)
            def circ_up_helper(d_px_i, r):
                return math.sqrt(math.fabs(r ** 2 - d_px_i ** 2))

            def circ_low_helper(d_px_i, r):
                return -circ_up_helper(d_px_i, r)

            def checking_values_x(r):
                c = [0, -r, r]
                if r == 3:
                    c.extend([2, -2])
                else:
                    mid = r / math.sqrt(2)
                    mf, mc =math.floor(mid), math.ceil(mid)
                    c.extend([mf, mc, -mf, -mc])
                return np.array(c)
            cvx = checking_values_x(r)
            ucv = np.array([circ_up_helper(cv, r) for cv in cvx])
            lcv = np.array([circ_low_helper(cv, r) for cv in cvx])

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
        return_val = np.array([np.array([get_point_coords(x) * cellsize, get_plant_type(x)], dtype=object)
                               for x in final_points])
        return return_val, points

    # Master Control Loop
    b_garden_points = None
    if bounds_map_creator_args == False:
        fill_final = True
    else:
        for bmca in bounds_map_creator_args:
            b_garden_points, points = generate_garden_cluster(
                beta, bmca, b_garden_points, points)
    if fill_final:
        b_garden_points, new_points_arr = generate_garden_cluster(
            beta, False, b_garden_points, points)
    # Timing
    stop = time.time()
    time_elapsed = stop - start
    global global_time_elapsed
    global_time_elapsed = time_elapsed
    return b_garden_points
