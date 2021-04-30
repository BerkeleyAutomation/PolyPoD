"""

Code that generates images.

"""

import numpy as np
from numpy.random import default_rng
rng = default_rng()
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('tkagg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
import mpl_toolkits

# Generates random 4x10x10 (plant_max_height by g...) images of dots and cirles, representing a 10x10 garden with 4 different
# plant species. the x dimension specifies plant type, the y and z specify the location of the plant,
# and the value entry represents the height of the plant.

garden_x_len = 10
garden_y_len = 10
plant_max_height = 2
plant_min_height = 0.5
garden_dimensions = (garden_x_len, garden_y_len, plant_max_height)
colors_of_plants = ["red", "yellow", "green", "blue"]
num_plants = 10
prob_of_plant = 0.25
alpha = 1

# Return random plant radius: for now, just 0.5, but later we can sample from a distribution
# or something.
def plant_radius():
    return rng.uniform(0.25, 1)

def plant_height(plant_type):

    return rng.uniform(plant_min_height, plant_max_height)

# Returns plant x, y, z, and radius from an iterator with multi-index, and the value returned by
# the iterator.
def get_plant_data(it, p):
    return it.multi_index[0], it.multi_index[1], p, plant_radius()

# Return color of plant
def get_plant_color(it):
    return colors_of_plants[it.multi_index[2]]

def plant_present(p):
    return not(p == 0)

def generate_random_images():
    r = []
    for _ in range(2):
        plant_present = rng.binomial(1, prob_of_plant, [garden_x_len,garden_y_len])
        plant_matrix = np.zeros((garden_x_len, garden_y_len, num_plants), dtype='int')
        it = np.nditer(plant_present, flags=["multi_index"])
        for x in it:
            if x == 1:
                plant_type = rng.integers(num_plants)
                plant_matrix[it.multi_index[0], it.multi_index[1], plant_type] = \
                    plant_height(plant_type)
        r.append(plant_matrix)
    return r

def plot_and_show_images(leftimage, rightimage, root):
    images_to_process = [leftimage, rightimage]
    figs = []
    axes = []
    for _ in range(len(images_to_process)):
        fig = Figure(figsize=(5, 4), dpi=100)
        figs.append(fig)
    canvases = pack_images(root, figs)
    for fig in figs:
        ax = fig.add_subplot(projection='3d')
        # Hide grid lines
        ax.grid(False)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        axes.append(ax)
    for ax in axes:
        #Axes3D only supports aspect arg 'auto'
        #ax.set_aspect(aspect=1)
        ax.set_xlim(left=-1, right=garden_x_len)
        ax.set_ylim(bottom=-1, top=garden_y_len)
        ax.set_zlim(bottom=0, top=plant_max_height)
    for _ in range(len(images_to_process)):
        img = images_to_process.pop()
        ax = axes.pop()

        it = np.nditer(img, flags=["multi_index", "refs_ok"])
        for p in it:
            if plant_present(p):
                x, y, z, r = get_plant_data(it, p)
                color = get_plant_color(it)

                # Cylinder
                x_num = 50
                z_step = 0.5
                rstride = 10
                cstride = 5
                cyl_x = np.linspace(x - r, x + r, x_num)
                cyl_z = np.arange(0, z + z_step, z_step)
                x_grid, z_grid = np.meshgrid(cyl_x, cyl_z, sparse=True)
                y_arc = np.sqrt(np.abs(r ** 2 - (abs(x_grid - x)) ** 2))
                y_grid_1 = y_arc + y
                y_grid_2 = -y_arc + y

                # Draw parameters
                ax.plot_surface(x_grid, y_grid_1, z_grid, alpha=alpha, rstride=rstride, cstride=cstride,
                                color=color, shade=True)
                ax.plot_surface(x_grid, y_grid_2, z_grid, alpha=alpha, rstride=rstride, cstride=cstride,
                                color=color, shade=True)

                # Top Circle
                circ_x_num = 10
                circ_r_num = 10
                rstride = 2
                cstride = 2
                circ_x = []
                circ_y_1 = []
                circ_y_2 = []
                for sub_r in np.linspace(0, r, circ_r_num):
                    sub_x = np.linspace(x - sub_r, x + sub_r, circ_x_num)
                    sub_y_arc = np.sqrt(np.abs(sub_r ** 2 - (abs(sub_x - x)) ** 2))
                    sub_y_1 = sub_y_arc + y
                    sub_y_2 = -sub_y_arc + y
                    circ_x.append(sub_x)
                    circ_y_1.append(sub_y_1)
                    circ_y_2.append(sub_y_2)
                circ_x = np.array(circ_x)
                circ_y_1 = np.array(circ_y_1)
                circ_y_2 = np.array(circ_y_2)
                circ_z_1 = np.full((circ_r_num, circ_x_num), z)
                circ_z_2 = np.full((circ_r_num, circ_x_num), 0)

                # draw
                ax.plot_surface(circ_x, circ_y_1, circ_z_1, alpha=alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
                ax.plot_surface(circ_x, circ_y_2, circ_z_1, alpha=alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)

                ax.plot_surface(circ_x, circ_y_1, circ_z_2, alpha=alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
                ax.plot_surface(circ_x, circ_y_2, circ_z_2, alpha=alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
    #pack_toolbars(root, canvases)

def pack_images(root, figs):
    for slave in root.pack_slaves():
        slave.pack_forget()
    canvases = []
    for count, fig in enumerate(figs):
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvases.append(canvas)

        # a somewhat hack-y solution to get the left image to pack on the left and the right image to
        # pack on the right.
        if count == 0:
            canvas.get_tk_widget().pack(side="left")
        else:
            canvas.get_tk_widget().pack(side="right")
    return canvases

def pack_toolbars(root, canvases):
    for canvas in canvases:
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()