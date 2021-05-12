# Poisson disc sampling in arbitrary dimensions via Bridson algorithm
# Implementation by Pavel Zun, pavel.zun@gmail.com
# BSD licence - https://github.com/diregoblin/poisson_disc_sampling

# -----------------------------------------------------------------------------
# Based on 2D sampling by Nicolas P. Rougier - https://github.com/rougier/numpy-book
# -----------------------------------------------------------------------------

import numpy as np
from scipy.special import gammainc
import garden_constants

default_radius = 0.05
num_of_each_plant = np.full(garden_constants.num_plants, 2)


def plant_height(self, plant_type):
    return garden_constants.plant_height_distribution_params[plant_type]

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
    return np.random.uniform(np.zeros(ndim), dims)

def squared_distance(p0, p1):
    return np.sum(np.square(p0-p1))

# returns (x, y) tuple and radius of plant
def get_point_info(p):
    return p[0], p[1]

def Bridson_sampling(dims=np.array([1.0,1.0]), radius=default_radius, k=30,
                     sample=uniform_sample):
    # References: Fast Poisson Disk Sampling in Arbitrary Dimensions
    #             Robert Bridson, SIGGRAPH, 2007

    ndim=dims.size

    # size of the sphere from which the samples are drawn relative to the size of a disc (radius)
    sample_factor = 2
    
    def in_limits(p):
        return np.all(np.zeros(ndim) <= p) and np.all(p < dims)

    # Check if there are samples closer than "squared_radius" to the candidate "p"
    def in_neighborhood(p, n=2):
        indices = (p / cellsize).astype(int)
        indmin = np.maximum(indices - n, np.zeros(ndim, dtype=int))
        indmax = np.minimum(indices + n + 1, gridsize)
        
        # Check if the center cell is empty
        if not np.isnan(P[tuple(indices)][0]):
            return True
        a = []
        for i in range(ndim):
            a.append(slice(indmin[i], indmax[i]))
        if np.any(np.sum(np.square(p - P[tuple(a)]), axis=ndim) < squared_radius):
            return True
    
    def add_point(x, y, r):
        points[x, y] = [1.0, x * cellsize, y * cellsize, r]

    def next_point():
        candidates = points[~np.isnan(points[:,:,0])][:,1:]
        return candidates[np.random.randint(candidates.shape[0])]

    cellsize = radius/np.sqrt(ndim)
    gridsize = (np.ceil(dims/cellsize)).astype(int)

    # points stores point locations:
    # points[x, y] = [b, x, y, r]
    # b = 1 if plant here, np.nan if not. cart_x, cart_y are location of plant in
    # standard coordinates,
    # r is inhibitive radius of plant. b, cart_x, cart_y, r are all False if there is no
    # plant at x, y.
    points = np.full(np.append(gridsize, ndim + 2), np.nan, dtype=np.float32) #n-dim value for each grid cell

    it = np.nditer(points, flags=["multi_index", "refs_ok"])
    for p in it:
        if it.multi_index[2] == 1:
            points[it.multi_index] = it.multi_index[0]
        elif it.multi_index[2] == 2:
            points[it.multi_index] = it.multi_index[1]
    x, y = uniform_sample(ndim, dims)
    plant_index = garden_constants.num_plants - 1
    add_point(x, y, plant_height(plant_index))

    while np.any(~np.isnan(points[:,:,0])) and plant_index >= 0:
        i = next_point()
        q = sample(ndim, dims)
        if in_limits(q) and not in_neighborhood(q):
            add_point(q)
    return points
