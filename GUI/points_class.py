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
