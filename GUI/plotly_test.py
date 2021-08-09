import plotly.graph_objects as go
import numpy as np
from SeedPlacementGenerators import RandomSeedPlacementGenerator
import garden_constants
from datetime import datetime
import combine_plotly_surfaces

# best y_eye_mult: doesn't make a difference if above 1
# best z_ratio: 0.375
# best h_hult: 0.43
data_to_load = ['datasets/dataset3/3_0_08-07-21_09-52-24-828566_data']
where_to_save = 'color_testing/'
single_values = {'y_eye_mult':10, 'h_mult':0.5,
               'z_ratio':0.42, 'plant_labels':False,
               'color_dict':garden_constants.color_custom_order}
color_of_soil = garden_constants.soil_color_atsu
hms = [0.5]
z_ratios = [1]
plant_labels = [True]
rotate_45 = [False]
text_offset = 3
colors_dicts = [garden_constants.color_custom_order]
shuffle_colors = False
save_value = False
dpi_scales = [4]
heights = []
widths = []
no_height_width = True
timestamp = True
from datetime import datetime
import re

def num_to_str(num):
    a = "{:.2f}".format(num)
    str_a = str(a)
    list_str_a = re.split(r'\.', str_a)
    if len(list_str_a) == 2:
        str_a = list_str_a[0] + "," + list_str_a[1]
    return str_a

def timestamp():
    return datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f")

def plotly_test(y_eye_mult, z_ratio, h_mult, colors_dict, cylinder_nt, void_size, where_to_save,
                data=None, plant_labels=True, save=True, rotate_45=False):
    assert len(colors_dict) == garden_constants.num_plants
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

    def cylinder(r, h, x, y, nt=cylinder_nt, nv=2):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        theta = np.linspace(0, 2*np.pi, nt)
        v = np.linspace(0, h, nv)
        theta, v = np.meshgrid(theta, v)
        x_g = (r*np.cos(theta)) + x
        y_g = (r*np.sin(theta)) + y
        z_g = v
        x_g = np.vstack((np.full(x_g.shape, x), x_g, np.full(x_g.shape, x)))
        y_g = np.vstack((np.full(y_g.shape, y), y_g, np.full(y_g.shape, y)))
        z_g = np.vstack((np.full(z_g.shape, 0), z_g, np.full(z_g.shape, h)))
        return x_g, y_g, z_g


    to_plot = []
    if data is None:
        data = np.load('test_plots/plotted_graph_data_05-25-21_22-50-47-167517.npy', allow_pickle=True)
    #it = np.nditer(data.seed_placement, flags=["multi_index", "refs_ok"])

    contours = go.surface.Contours(
                x=go.surface.contours.X(highlight=False),
                y=go.surface.contours.Y(highlight=False),
                z=go.surface.contours.Z(highlight=False),
            )

    to_plot = []

    for p in data:
        loc, plant_index, r = garden_constants.point_unpacker(p)
        x, y = loc
        color = colors_dict[plant_index]
        colorscale = make_colorscale(color)
        if plant_index == 0:
            xc, yc, zc = cylinder(void_size, 0.01, x, y)
        else:
            xc, yc, zc = cylinder(r, h_mult * r, x, y)

        cyl = go.Surface(x=xc, y=yc, z=zc,
                         colorscale=colorscale,
                         showscale=False,
                         opacity=1,
                         hoverinfo='none',
                         contours=contours)
        to_plot.append(cyl)

    # FOR SCALING PURPOSES: invisible cylinder to prevent over-zooming
    color = colors_dict[1]
    colorscale = make_colorscale(color)
    scale_cyl_r = 290
    xc, yc, zc = cylinder(scale_cyl_r, h_mult * r, garden_constants.garden_x_len / 2, garden_constants.garden_x_len / 2)

    cyl = go.Surface(x=xc, y=yc, z=zc,
                     colorscale=colorscale,
                     showscale=False,
                     opacity=0,
                     hoverinfo='none',
                     contours=contours)
    to_plot.append(cyl)

    if rotate_45:
        scale_in = 55
        for x in [scale_in + -garden_constants.garden_x_len / 2, -scale_in + 3 * garden_constants.garden_x_len / 2]:
            for y in [scale_in + -garden_constants.garden_y_len / 2, -scale_in + 3 * garden_constants.garden_y_len / 2]:
                xc, yc, zc = cylinder(1, h_mult * r, x, y)

                cyl = go.Surface(x=xc, y=yc, z=zc,
                                 colorscale=colorscale,
                                 showscale=False,
                                 opacity=0,
                                 hoverinfo='none',
                                 contours=contours)
                to_plot.append(cyl)

    x_soil = np.array([[0, garden_constants.garden_x_len], [0, garden_constants.garden_x_len]])
    y_soil = np.array([[0, 0], [garden_constants.garden_x_len, garden_constants.garden_x_len]])
    z_soil = np.array([[0,0], [0,0]])

    soil = go.Surface(x=x_soil, y=y_soil, z=z_soil,
                     colorscale=make_colorscale(color_of_soil),
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
                       margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                       scene_xaxis_visible=False,
                       scene_yaxis_visible=False,
                       scene_zaxis_visible=False)

    y_eye = y_eye_mult * garden_constants.garden_x_len
    z_eye = y_eye * z_ratio
    x_eye = y_eye if rotate_45 else 0
    camera = dict(
        eye=dict(x=x_eye, y=-y_eye, z=z_eye)
    )
    to_plot.append(soil)

    # opacity =0.9 - many overlaped areas, better witot it
    fig = go.Figure(data=to_plot, layout=layout)

    if plant_labels:
        def get_x_labels(data):
            return [p[0][0] for p in data]

        def get_y_labels(data):
            return [p[0][1] for p in data]

        def get_z_labels(data):
            return [garden_constants.plant_radii[p[1]] * h_mult + text_offset for p in data]

        def get_text_labels(data):
            return [str(int(p[1])) for p in data]
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
        for dpi_scale in dpi_scales:
            fig.write_image(where_to_save + f'h_mult_{num_to_str(h_mult)}_z_ratio_{num_to_str(z_ratio)}_3d_{timestamp() if timestamp else ""}.png', scale=dpi_scale)
    else:
        fig.show()

def main(mode):
    if mode == 'cross':
        print(f'num images: {len(data_to_load) * len(hms) * len(z_ratios) * len(colors_dicts) * len(plant_labels) * len(rotate_45)}')
        for d in data_to_load:
            loaded_data = np.load(d, allow_pickle=True)
            seed_placement_data = loaded_data['data']
            for hm in hms:
                for z_ratio in z_ratios:
                    for colors_dict in colors_dicts:
                        for plant_label in plant_labels:
                            for r in rotate_45:
                                plotly_test(y_eye_mult=single_values['y_eye_mult'], z_ratio=z_ratio, h_mult=hm,
                                            colors_dict=colors_dict, plant_labels=plant_label, data=seed_placement_data,
                                    where_to_save=where_to_save,
                                    cylinder_nt=70, void_size=loaded_data['void_size'], rotate_45=r)
    elif mode == 'single':
        for d in data_to_load:
            loaded_data = np.load(d, allow_pickle=True)
            seed_placement_data = loaded_data['data']
            plotly_test(single_values['y_eye_mult'],
                        single_values['z_ratio'],
                        single_values['h_mult'],
                        single_values['color_dict'],
                        plant_labels=False,
                        data=seed_placement_data,
                        where_to_save=where_to_save,
                        cylinder_nt=70, void_size=loaded_data['void_size'])

if __name__ == '__main__':
    main('cross')