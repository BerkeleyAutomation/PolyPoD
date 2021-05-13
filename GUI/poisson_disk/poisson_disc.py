# Poisson disc sampling in arbitrary dimensions via Bridson algorithm
# Implementation by Pavel Zun, pavel.zun@gmail.com
# BSD licence - https://github.com/diregoblin/poisson_disc_sampling

# -----------------------------------------------------------------------------
# Based on 2D sampling by Nicolas P. Rougier - https://github.com/rougier/numpy-book
# -----------------------------------------------------------------------------

import numpy as np
from scipy.special import gammainc
import garden_constants
import math
from numpy.random import default_rng
rng = default_rng()


# Uniform sampling in a hypersphere
# Based on Matlab implementation by Roger Stafford
# Can be optimized for Bridson algorithm by excluding all points within the r/2 sphere
def hypersphere_volume_sample(center,radius,k=1):
    ndim = center.size
    x = np.random.normal(size=(k, ndim))
    ssq = np.sum(x**2,axis=1)
    fr = radius*gammainc(ndim/2,ssq/2)**(1/ndim)/np.sqrt(ssq)
    frtiled = np.tile(fr.reshape(k,1),(1,ndim))
    p = center + np.multiply(x,frtiled)
    return p


# Uniform sampling on the sphere's surface
def hypersphere_surface_sample(center,radius,k=1):
    ndim = center.size
    vec = np.random.standard_normal(size=(k, ndim))
    vec /= np.linalg.norm(vec, axis=1)[:,None]
    p = center + np.multiply(vec, radius)
    return p

def uniform_sample(ndim, dims):
    s = rng.integers(dims)
    return s

def squared_distance(p0, p1):
    return np.sum(np.square(p0-p1))


def vrpd(dims, num_of_each_plant, plant_radii, cellsize):
    ndim = dims.size
    dims = (dims / cellsize).astype(int)
    def inhibition_radius(plant_type):
        return garden_constants.plant_height_distribution_params[plant_type] / cellsize
    def next_point(plant_type):
        r = inhibition_radius(plant_type)
        pm = plant_map(points)
        cpm = cp_map(points)
        c1 = np.isnan(pm)
        c2 = cpm >= r
        criteria = (c1 & c2)
        candidates = points[criteria]
        if len(candidates) == 0:
            return False
        choice = candidates[rng.integers(candidates.shape[0])]
        add_point(point_coords(choice), r, plant_type)
        return True
    def add_point(choice, r, plant_type):
        x, y = choice
        pl = point_list(points)
        for p in pl:
            px, py = point_coords(p)
            d = math.dist(choice, [px, py])
            if d < cp(p):
                set_cp(px, py, d)
            if d < r:
                mark_blocked(px, py)
        mark_plant(x, y, plant_type)

    # points stores point locations:
    # points[x, y] = [b, x, y, cp, t]
    # b = 1.0 if plant here, 2.0 if point is blocked, np.nan if no plant.
    # x, y is loc of plant
    # cp is distanct to closest plant
    # t is type of plant, as plant index
    points = np.full(np.append(dims, ndim + 3), np.nan, dtype=np.float32)
    it = np.nditer(points, flags=["multi_index", "refs_ok"])
    for p in it:
        if it.multi_index[2] == 1:
            points[it.multi_index] = it.multi_index[0]
        elif it.multi_index[2] == 2:
            points[it.multi_index] = it.multi_index[1]
        elif it.multi_index[2] == 3:
            points[it.multi_index] = np.inf
    def plant_map(points):
        return points[:,:,0]
    def point_coords(p):
        return p[1:3]
    def cp(p):
        return p[3]
    def plant_type(p):
        return p[4]
    def set_cp(x, y, cp):
        points[int(x), int(y), 3] = cp
    def mark_plant(x, y, t):
        points[int(x), int(y), 0] = 1.0
        points[int(x), int(y), 4] = t
    def mark_blocked(x, y):
        points[int(x), int(y), 0] = 2.0
    def cp_map(points):
        return points[:,:,3]
    def point_list(points):
        return points.reshape(points.shape[0] * points.shape[1], points.shape[2])

    x, y = uniform_sample(ndim, dims)
    plant_index = garden_constants.num_plants - 1
    add_point([x, y], inhibition_radius(plant_index), plant_index)
    num_of_each_plant[plant_index] -= 1
    while plant_index >= 0:
        for _ in range(num_of_each_plant[plant_index]):
            n = next_point(plant_index)
            if not n:
                break
        plant_index -= 1

    # to cartesian
    plant_map = plant_map(points)
    final_points = points[plant_map == 1.0]
    final_points = np.array([np.array([point_coords(x) * cellsize, plant_type(x)], dtype=object) for x in final_points])
    return final_points

