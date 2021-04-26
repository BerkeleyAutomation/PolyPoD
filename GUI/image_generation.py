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

# Generates random 4x10x10 (garden_z_len by g...) images of dots and cirles, representing a 10x10 garden with 4 different
# plant species. the x dimension specifies plant type, the y and z specify the location of the plant,
# and the value entry represents the height of the plant.

garden_x_len = 8
garden_y_len = 15
garden_z_len = 5
garden_dimensions = (garden_x_len, garden_y_len, garden_z_len)
colors_of_plants = ["red", "yellow", "green", "blue"]
num_plants = 4
prob_of_plant = 0.05

# Return random plant radius: for now, just 0.5, but later we can sample from a distribution
# or something.
def plant_radius():
    return 0.5

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
                plant_matrix[it.multi_index[0], it.multi_index[1], rng.integers(4)] = \
                    rng.integers(garden_z_len)
        r.append(plant_matrix)
    return r

def plot_and_show_images(leftimage, rightimage, root):
    images_to_process = [leftimage, rightimage]
    figs = []
    axes = []
    for _ in range(len(images_to_process)):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        figs.append(fig)
        axes.append(ax)

    for ax in axes:
        #Axes3D only supports aspect arg 'auto'
        #ax.set_aspect(aspect=1)
        ax.set_xlim(left=-1, right=garden_x_len)
        ax.set_ylim(bottom=-1, top=garden_y_len)
        ax.set_zlim(bottom=0, top=garden_z_len)
    for _ in range(len(images_to_process)):
        img = images_to_process.pop()
        ax = axes.pop()

        it = np.nditer(img, flags=["multi_index", "refs_ok"])
        for p in it:
            if plant_present(p):
                x, y, z, r = get_plant_data(it, p)
                color = get_plant_color(it)

                # Cylinder
                x_space = 100
                z_step = 0.2
                cyl_x = np.linspace(x - r, x + r, x_space)
                cyl_z = np.arange(0, z + z_step, z_step)
                x_grid, z_grid = np.meshgrid(cyl_x, cyl_z)
                y_arc = np.sqrt(r ** 2 - (abs(x_grid - x)) ** 2)
                y_grid_1 = y_arc + y
                y_grid_2 = -y_arc + y

                # Draw parameters
                rstride = 20
                cstride = 10
                ax.plot_surface(x_grid, y_grid_1, z_grid, alpha=0.9, rstride=rstride, cstride=cstride,
                                color=color)
                ax.plot_surface(x_grid, y_grid_2, z_grid, alpha=0.9, rstride=rstride, cstride=cstride,
                                color=color)
        pack_images(root, figs)

def pack_images(root, figs):
    for slave in root.pack_slaves():
        slave.pack_forget()

    for count, fig in enumerate(figs):
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()

        # a somewhat hack-y solution to get the left image to pack on the left and the right image to
        # pack on the right.
        if count == 0:
            canvas.get_tk_widget().pack(side="left")
        else:
            canvas.get_tk_widget().pack(side="right")