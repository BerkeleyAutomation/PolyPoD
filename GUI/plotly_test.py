import plotly.graph_objects as go
import numpy as np
from SeedPlacementGenerators import RandomSeedPlacementGenerator
import garden_constants

def make_colorscale(color):
    return [[0, color], [1, color]]

def cylinder(r, h, x, y, nt=20, nv=2):
    """
    parametrize the cylinder of radius r, height h, base point a
    """
    theta = np.linspace(0, 2*np.pi, nt)
    v = np.linspace(0, h, nv)
    theta, v = np.meshgrid(theta, v)
    x_g = (r*np.cos(theta)) + x
    y_g = (r*np.sin(theta)) + y
    z_g = v
    return x_g, y_g, z_g

def boundary_circle(r, h, x, y, nt=20, nr=2):
    """
    r - boundary circle radius
    h - height above xOy-plane where the circle is included
    x, y - centerpoint
    returns the circle parameterization
    """
    theta = np.linspace(0, 2 * np.pi, nt)
    r = np.linspace(0, r, nr)
    theta, r = np.meshgrid(theta, r)
    x_g = (r * np.cos(theta)) + x
    y_g = (r * np.sin(theta)) + y
    z_g = h*np.ones(theta.shape)
    return x_g, y_g, z_g

to_plot = []
spg = RandomSeedPlacementGenerator.RandomSeedPlacementGenerator(prob_of_plant=0.05)
img = spg.generate_seed_placement()
it = np.nditer(img.seed_placement, flags=["multi_index", "refs_ok"])

contours = go.surface.Contours(
            x=go.surface.contours.X(highlight=False),
            y=go.surface.contours.Y(highlight=False),
            z=go.surface.contours.Z(highlight=False),
        )

for p in it:
    if img.plant_present(p):
        x, y, h, r = img.get_plant_data(it, p)
        color = img.get_plant_color(it)
        colorscale = make_colorscale(color)

        xc, yc, zc = cylinder(r, h, x, y)

        xcircl, ycircl, zcircl = boundary_circle(r, 0, x, y)
        xcirch, ycirch, zcirch = boundary_circle(r, h, x, y)


        cyl = go.Surface(x=xc, y=yc, z=zc,
                         colorscale=colorscale,
                         showscale=False,
                         opacity=1,
                         hoverinfo='none',
                         contours=contours)
        circl = go.Surface(x=xcircl, y=ycircl, z=zcircl,
                           colorscale=colorscale,
                           showscale=False,
                           opacity=1,
                           hoverinfo='none',
                           contours=contours)
        circh = go.Surface(x=xcirch, y=ycirch, z=zcirch,
                           colorscale=colorscale,
                           showscale=False,
                           opacity=1,
                           hoverinfo='none',
                           contours=contours)
        to_plot.extend([cyl, circl, circh])

x_soil = np.array([[0, 10], [0, 10]])
y_soil = np.array([[0, 0], [10, 10]])
z_soil = np.array([[0,0], [0,0]])
soil = go.Surface(x=x_soil, y=y_soil, z=z_soil,
                 colorscale=make_colorscale(garden_constants.soil_color),
                 showscale=False,
                 opacity=1,
                 hoverinfo='none',
                  contours=contours)
to_plot.append(soil)

scene=go.layout.Scene(
        xaxis=go.layout.scene.XAxis(
            spikecolor='#1fe5bd',
            showspikes=False,
            spikethickness=0,
        ),
        yaxis=go.layout.scene.YAxis(
            spikecolor='#1fe5bd',
            showspikes=False,
            spikethickness=0,
        ),
        zaxis=go.layout.scene.ZAxis(
            spikecolor='#1fe5bd',
            showspikes=False,
            spikethickness=0,
        ),
        aspectmode='data'
)
layout = go.Layout(scene=scene,
                   scene_xaxis_visible=False,
                   scene_yaxis_visible=False,
                   scene_zaxis_visible=False)
fig = go.Figure(data=to_plot, layout=layout)
fig.update_traces(hoverinfo='none')
fig.update_layout(scene_camera_eye_z=0.55)

fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

fig.show()
