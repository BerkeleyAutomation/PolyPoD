import numpy as np
import plotly.graph_objs as go
import plotly_test as pt

# normalize values to range [start,end] for getting color from cmap
def norm_v_in_range(v, start, end):
    v_min = v.min()
    v_max = v.max()
    range_length = (end - start)

    if v_min - v_max == 0:
        v.fill(range_length / 5 + start)
        return v

    return (v - v_min) / (v_max - v_min) * range_length + start

def make_square(XYZ):
    x_max = 0
    y_max = 0
    z_max = 0
    for s in XYZ:
        x_max = max(len(s[0][0]), x_max)
        y_max = max(len(s[1][0]), y_max)
        z_max = max(len(s[2][0]), z_max)
    def fix_z(z):
        z = np.array([np.append(r, np.full(x_max - len(r), np.nan)) for r in z])
        to_add = np.full((y_max - z.shape[0], x_max), 0)
        z = np.concatenate((z, to_add), axis=0)
        return z

    XYZ = [[np.append(s[0], np.full(x_max - len(s[0]), np.nan)),
            np.append(s[1], np.full(y_max - len(s[1]), np.nan)),
            fix_z(s[2])] for s in XYZ]

    return XYZ

def combine_all_surfaces_in_one(XYZ, color):
    # prepare colors and ranges for diffrent surfaces
    custom_colorscale = [[0, color], [1, color]]

    X0 = XYZ[0][0]
    Y0 = XYZ[0][1]
    Z0 = XYZ[0][2]

    # transparent connection between grahps: np.nan in z prevent ploting points
    transparen_link = np.empty_like(X0[0], dtype=object)
    transparen_link.fill(np.nan)

    # include first graph
    combined_X = X0
    combined_Y = Y0
    combined_Z = Z0

    for i, next_surf in enumerate(XYZ[1:]):
        X = next_surf[0]
        Y = next_surf[1]
        Z = next_surf[2]
        combined_X = np.vstack([combined_X, combined_X[-1], X[0], X])
        combined_Y = np.vstack([combined_Y, combined_Y[-1], Y[0], Y])
        combined_Z = np.vstack([combined_Z, transparen_link, transparen_link, Z])

    return combined_X, combined_Y, combined_Z, custom_colorscale


X_nongrid = np.arange(-1.2, 1.06, 0.1)
Y_nongrid = np.arange(0.2, 1.06, 0.1)
X, Y = np.meshgrid(X_nongrid, Y_nongrid)

X2_nongrid = np.arange(-0.2, 2, 0.1)
Y2_nongrid = np.arange(-1, 2, 0.1)
X2, Y2 = np.meshgrid(X2_nongrid, Y2_nongrid)

Z1 = 2 * np.sin(np.sqrt(20 * X ** 2 + 20 * Y ** 2))
Z2 = 2 * np.cos(np.sqrt(20 * X2 ** 2 + 20 * Y2 ** 2))
Z3 = X * 2 + 0.5
Z4 = Y * 0 + 1.0
Z5 = Y * 0 - 1.0
Z6 = Y * 1 + 10
inputs = [[X_nongrid, Y_nongrid, Z1], [X2_nongrid, Y2_nongrid, Z2], [X_nongrid, Y_nongrid, Z3], [X_nongrid, Y_nongrid, Z4], [X_nongrid, Y_nongrid, Z5], [X_nongrid, Y_nongrid, Z6]]

if __name__ == '__main__':
    x, y, z, custom_surfacecolor, custom_colorscale = combine_all_surfaces_in_one(inputs)


    # opacity =0.9 - many overlaped areas, better witot it
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z,
                                     surfacecolor=custom_surfacecolor, cmin=0, cmax=1,
                                     colorscale=custom_colorscale, showscale=False,
                                     )])

    fig.show()
