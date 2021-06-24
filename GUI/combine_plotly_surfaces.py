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

def combine_all_surfaces_in_one(X, Y, *Z):
    # prepare colors and ranges for diffrent surfaces
    colors = ['rgb(180, 110,  20)', 'rgb( 20, 180, 110)', 'rgb(110, 20, 180)',
              'rgb(180, 180,  20)', 'rgb( 20, 180, 180)', 'rgb(180, 20, 180)',
              'rgb(180,  20,  20)', 'rgb( 20, 180,  20)', 'rgb( 20, 20, 180)',
              'rgb(180, 110,  20)', 'rgb( 20, 180, 110)', 'rgb(110, 20, 180)',
              'rgb(255, 127, 127)', 'rgb(127, 255, 127)']

    N = len(Z)
    points = np.linspace(0, 1, N + 1)
    custom_colorscale = []
    ranges = []

    for i in range(1, N + 1):
        ranges.append([points[i - 1], points[i] - 0.05])
        custom_colorscale.append([points[i - 1], colors[i]])
        custom_colorscale.append([points[i] - 0.05, colors[i]])
    custom_colorscale.append([1, colors[i]])

    # transparent connection between grahps: np.nan in z prevent ploting points
    transparen_link = np.empty_like(X[0], dtype=object)
    transparen_link.fill(np.nan)

    # include first graph
    combined_X = X
    combined_Y = Y
    combined_Z = Z[0]

    # prepare collor matrix for first graph (Z[0])
    start = ranges[0][0]
    end = ranges[0][1]

    custom_surfacecolor = norm_v_in_range(Z[0], start, end)

    # second aray combined with first in backward direction, so connection would on one side of graphs, not intersect them
    direction = -1

    range_index = 1

    for next_Z in Z[1:]:
        combined_X = np.vstack([combined_X, combined_X[-1], X[::direction][0], X[::direction][0], X[::direction]])
        combined_Y = np.vstack([combined_Y, combined_Y[-1], Y[::direction][0], Y[::direction][0], Y[::direction]])
        combined_Z = np.vstack(
            [combined_Z, combined_Z[-1], transparen_link, next_Z[::direction][0], next_Z[::direction]])

        # prepare collors for next Z_
        start = ranges[range_index][0]
        end = ranges[range_index][1]
        next_surfacecolor = norm_v_in_range(next_Z, start, end)
        custom_surfacecolor = np.vstack(
            [custom_surfacecolor, custom_surfacecolor[-1], transparen_link, next_surfacecolor[::direction][0],
             next_surfacecolor[::direction]])

        # change direction
        direction *= -1

        range_index += 1

    return combined_X, combined_Y, combined_Z, custom_surfacecolor, custom_colorscale


X = np.arange(-1.2, 1.06, 0.1)
Y = np.arange(0.2, 1.06, 0.1)
X, Y = np.meshgrid(X, Y)

Z1 = 2 * np.sin(np.sqrt(20 * X ** 2 + 20 * Y ** 2))
Z2 = 2 * np.cos(np.sqrt(20 * X ** 2 + 20 * Y ** 2))
Z3 = X * 2 + 0.5
Z4 = Y * 0 + 1.0
Z5 = Y * 0 - 1.0
Z6 = Y * 1 + 10
x, y, z, custom_surfacecolor, custom_colorscale = combine_all_surfaces_in_one(X, Y, Z1, Z2, Z3, Z4, Z5, Z6)

# opacity =0.9 - many overlaped areas, better witot it
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z,
                                 surfacecolor=custom_surfacecolor, cmin=0, cmax=1,
                                 colorscale=custom_colorscale, showscale=False,
                                 )])

fig.show()