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

def generate_random_images():
    r = []
    for _ in range(2):
        plant_present = rng.binomial(1, 0.3, [garden_x_len,garden_y_len])
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
    """ one image version
    images_to_process = [leftimage]
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    axes = [ax]
    """
    for ax in axes:
        #Axes3D only supports aspect arg 'auto'
        #ax.set_aspect(aspect=1)
        ax.set_xlim(left=-1, right=garden_x_len)
        ax.set_ylim(bottom=-1, top=garden_y_len)
        ax.set_zlim(bottom=-1, top=garden_z_len)
    for _ in range(len(images_to_process)):
        img = images_to_process.pop()
        ax = axes.pop()

        colors = np.full(garden_dimensions, None, dtype=object)
        voxels = np.full(garden_dimensions, False, dtype=object)

        it = np.nditer(img, flags=["multi_index"])
        for p in it:
            if not(p == 0):
                voxels[it.multi_index[0], it.multi_index[1], p] = True
                colors[it.multi_index[0], it.multi_index[1], p] = colors_of_plants[
                    it.multi_index[2]]
        ax.voxels(voxels, facecolors=colors)

        """ the old version: scatter
        colors_of_plants = ["red", "yellow", "green", "blue"]
        coords_of_plants = [[],[],[],[]]
        it = np.nditer(img, flags=["multi_index"])

        for x in it:
            if not(x == 0):
                coords_of_plants[it.multi_index[0]].append([it.multi_index[1], it.multi_index[2], x])

        for p in coords_of_plants:
            x, y, z = zip(*p)
            ax.scatter(x, y, z, color=colors_of_plants.pop())
        """
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