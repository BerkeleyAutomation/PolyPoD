import plotly.graph_objects as go
import numpy as np
from SeedPlacementGenerators import RandomSeedPlacementGenerator
import garden_constants
from datetime import datetime
import combine_plotly_surfaces

# best y_eye_mult: doesn't make a difference if above 1
# best z_ratio: 0.375
# best h_hult: 0.43
data_to_load = ['french_plots/data_06-24-21_16-54-29-226489.npy']
where_to_save = 'french_plots'
single_values = {'y_eye_mult':10, 'h_mult':0.43,
               'z_ratio':0.42, 'plant_labels':False,
               'color_dict':garden_constants.colors_of_plants_hcl_v2}
hms = [single_values['h_mult']]
z_ratios = [single_values['z_ratio']]
plant_labels = [False]
text_offset = 0.3
colors_dicts = [single_values['color_dict']]
shuffle_colors = True
save_value = False

def plotly_test(y_eye_mult, z_ratio, h_mult, colors_dict, data=False, plant_labels=True, save=True,
                where_to_save=False):
    if shuffle_colors:
        copy = [x for x in range(len(colors_dict))]
        for r in range(3):
            for c in range(3):
                new_c = 2 - r
                new_r = c
                copy[3 * new_r + new_c] = colors_dict[3 * r + c]
        copy[9] = colors_dict[9]
        colors_dict = copy
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
        x_g = np.vstack((np.full((1, x_g.shape[1]), x), x_g, np.full((1, x_g.shape[1]), x)))
        y_g = np.vstack((np.full((1, y_g.shape[1]), y), y_g, np.full((1, y_g.shape[1]), y)))
        z_g = np.vstack((np.full((1, z_g.shape[1]), 0), z_g, np.full((1, z_g.shape[1]), h)))
        return x_g, y_g, z_g


    if data is None:
        data = np.load('test_plots/plotted_graph_data_05-25-21_22-50-47-167517.npy', allow_pickle=True)
    #it = np.nditer(data.seed_placement, flags=["multi_index", "refs_ok"])

    contours = go.surface.Contours(
                x=go.surface.contours.X(highlight=False),
                y=go.surface.contours.Y(highlight=False),
                z=go.surface.contours.Z(highlight=False),
            )

    to_plot = [[] for _ in range(10)]
    for p in data:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        x, y = loc
        color = colors_dict[plant_index]
        colorscale = make_colorscale(color)

        xc, yc, zc = cylinder(r, h_mult * r, x, y)

        '''
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
        '''
        to_plot[plant_index].append([xc, yc, zc])

    x_soil = np.array([[0, garden_constants.garden_x_len], [0, garden_constants.garden_x_len]])
    y_soil = np.array([[0, 0], [garden_constants.garden_y_len, garden_constants.garden_y_len]])
    z_soil = np.array([[0,0], [0,0]])

    soil = go.Surface(x=x_soil, y=y_soil, z=z_soil,
                     colorscale=make_colorscale(garden_constants.soil_color),
                     showscale=False,
                     opacity=1,
                     hoverinfo='none',
                      contours=contours)

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
    surfaces = [soil]
    etp = list(enumerate(to_plot))
    print(colors_dict)
    for i, t in etp:
        if len(t) > 0:
            x, y, z, custom_colorscale = \
                combine_plotly_surfaces.combine_all_surfaces_in_one(t, colors_dict[i])
            surfaces.append(go.Surface(x=x, y=y, z=z,
                                     colorscale=make_colorscale(colors_dict[i]), showscale=False,
                                     opacity=1,
                                     hoverinfo='none',
                                     contours=contours
                                     ))

    # opacity =0.9 - many overlaped areas, better witot it
    fig = go.Figure(data=surfaces, layout=layout)

    if plant_labels:
        def get_x_labels(data):
            return [p[0][0] for p in data]

        def get_y_labels(data):
            return [p[0][1] for p in data]

        def get_z_labels(data):
            return [garden_constants.plant_radii[p[1]] * h_mult + text_offset for p in data]

        def get_text_labels(data):
            return [str(p[1]) for p in data]
        x_data = get_x_labels(data)
        y_data = get_y_labels(data)
        z_data = get_z_labels(data)
        text_labels = get_text_labels(data)
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
    fig.update_layout(scene_camera=camera)

    fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

    if save:
        if where_to_save:
            fig.write_image("3d_plot_{0}.png".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f")))
        else:
            fig.write_image("3d_plots/3d_plot_{0}.png".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f")))
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
        for d in data_to_load:
            loaded_data = np.load(d, allow_pickle=True)
            plotly_test(single_values['y_eye_mult'],
                        single_values['z_ratio'],
                        single_values['h_mult'],
                        single_values['color_dict'],
                        plant_labels=False,
                        data=loaded_data,
                        where_to_save=where_to_save,
                        save=save_value)

if __name__ == '__main__':
    main('single')