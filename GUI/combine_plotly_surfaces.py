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


def combine_all_surfaces_in_one(XYZC, colors):
    # prepare colors and ranges for diffrent surfaces
    XYZ = [a[:3] for a in XYZC]
    N = len(colors)
    points = np.linspace(0, 1, N + 1)
    custom_colorscale = []
    ranges = []

    X0 = XYZ[0][0]
    Y0 = XYZ[0][1]
    #X0, Y0 = np.meshgrid(X0, Y0)
    Z0 = XYZ[0][2]
    C0 = XYZC[3]
    for i in range(0, N):
        custom_colorscale.append([points[i], colors[i]])
    #custom_colorscale.append([1, XYZC[i - 1][3]]) # todo did commenting this screw something up?

    # transparent connection between grahps: np.nan in z prevent ploting points
    transparen_link = np.empty_like(X0[0], dtype=object)
    transparen_link.fill(np.nan)

    # include first graph
    combined_X = X0
    combined_Y = Y0
    combined_Z = Z0

    # prepare collor matrix for first graph (Z[0])
    start = ranges[0][0]
    end = ranges[0][1]

    custom_surfacecolor = norm_v_in_range(Z0, start, end)

    range_index = 1

    for next_surf in XYZ[1:]:
        X = next_surf[0]
        Y = next_surf[1]
        #X, Y = np.meshgrid(X, Y)
        Z = next_surf[2]
        #print('X\n', X, '\nY\n', Y, '\nZ\n', Z)
        combined_X = np.vstack([combined_X, combined_X[-1], X[0], X[0], X])
        combined_Y = np.vstack([combined_Y, combined_Y[-1], Y[0], Y[0], Y])
        combined_Z = np.vstack(
            [combined_Z, combined_Z[-1], transparen_link, Z[0], Z])

        # prepare collors for next Z_
        start = ranges[range_index][0]
        end = ranges[range_index][1]
        next_surfacecolor = np.full
        custom_surfacecolor = np.vstack(
            [custom_surfacecolor, custom_surfacecolor[-1], transparen_link, next_surfacecolor[0],
             next_surfacecolor])


        range_index += 1

    return combined_X, combined_Y, combined_Z, custom_surfacecolor, custom_colorscale


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
