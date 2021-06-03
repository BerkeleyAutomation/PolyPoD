import plotly.graph_objects as go
import numpy as np
from SeedPlacementGenerators import RandomSeedPlacementGenerator
import garden_constants
from datetime import datetime

# best y_eye_mult: doesn't make a difference if above 1
# best z_ratio: 0.375
# best h_hult: 0.43
best_values = {'y_eye_mult':1, 'h_mult':0.43,
               'z_ratio':0.42}
colors_dicts = [garden_constants.colors_of_plants_hcl_v2]
num_cols = 3
num_rows = (garden_constants.num_plants - 1) // num_cols + 1
shuffle_colors = True
if shuffle_colors:
    for colors_dict in colors_dicts:
        copy = [_ for x in range(colors_dict)]
        for r in num_rows:
            to_swap = colors_dict[num_cols * r: num_cols * (r + 1)]

            for n in to_swap:
                copy[]


hms = [0.25, 0.3, 0.35]
z_ratios = [0.375, 0.44, 0.5]
plant_labels = [True, False]
text_offset = 0.3
def plotly_test(y_eye_mult, z_ratio, h_mult, colors_dict, plant_labels=True, save=True):
    plotly_prob_of_plant = 0.02

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
    spg = RandomSeedPlacementGenerator.RandomSeedPlacementGenerator(
        prob_of_plant=plotly_prob_of_plant)
    img = np.load('test_plots/plotted_graph_data_05-25-21_22-50-47-167517.npy', allow_pickle=True)
    #it = np.nditer(img.seed_placement, flags=["multi_index", "refs_ok"])

    contours = go.surface.Contours(
                x=go.surface.contours.X(highlight=False),
                y=go.surface.contours.Y(highlight=False),
                z=go.surface.contours.Z(highlight=False),
            )

    for p in img:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        x, y = loc
        color = colors_dict[plant_index]
        colorscale = make_colorscale(color)

        xc, yc, zc = cylinder(r, h_mult * r, x, y)

        xcircl, ycircl, zcircl = boundary_circle(r, 0, x, y)
        xcirch, ycirch, zcirch = boundary_circle(r, h_mult * r, x, y)


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

    x_soil = np.array([[0, garden_constants.garden_x_len], [0, garden_constants.garden_x_len]])
    y_soil = np.array([[0, 0], [garden_constants.garden_y_len, garden_constants.garden_y_len]])
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

    y_eye = y_eye_mult * garden_constants.garden_x_len
    z_eye = y_eye * z_ratio
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=0, y=-y_eye, z=z_eye)
    )
    title_text = "z ratio: {0}; h_mult: {1}".format(z_ratio, h_mult)
    fig = go.Figure(data=to_plot, layout=layout)

    if plant_labels:
        def get_x_labels(img):
            return [p[0][0] for p in img]

        def get_y_labels(img):
            return [p[0][1] for p in img]

        def get_z_labels(img):
            return [garden_constants.plant_radii[p[1]] * h_mult + text_offset for p in img]

        def get_text_labels(img):
            return [str(p[1]) for p in img]
        x_data = get_x_labels(img)
        y_data = get_y_labels(img)
        z_data = get_z_labels(img)
        text_labels = get_text_labels(img)
        fig.add_trace(go.Scatter3d(
            x=x_data,
            y=y_data,
            z=z_data,
            mode="text",
            text=text_labels,
            textposition="middle center",
            textfont=dict(
                family="sans serif",
                size=12,
                color="red"
            )
        ))

    fig.update_traces(hoverinfo='none')
    fig.update_layout(scene_camera=camera, title_text=title_text)

    fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

    if save:
        fig.write_image("3d_plots/plotted_graph_{0}.png".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f")))
    else:
        fig.show()

def main(mode):
    if mode == 'cross':
        for hm in hms:
            for z_ratio in z_ratios:
                for colors_dict in colors_dicts:
                    for plant_label in plant_labels:
                        plotly_test(1, z_ratio, hm, colors_dict, plant_label, save=True)
    elif mode == 'single':
        plotly_test(best_values['y_eye_mult'],
                    best_values['z_ratio'],
                    best_values['h_mult'])

main('single')
