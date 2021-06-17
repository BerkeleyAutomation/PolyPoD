"""

Code that displays gardens

"""

import numpy as np
from numpy.random import default_rng
rng = default_rng()
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('tkagg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backend_bases import key_press_handler
import mpl_toolkits
import plotly.graph_objects as go
import garden_constants
import tkinter as tk
from PIL import ImageTk,Image

# Generates random 4x10x10 (plant_max_radius by g...) images of dots and cirles, representing a 10x10 garden with 4 different
# plant species. the x dimension specifies plant type, the y and z specify the location of the plant,
# and the value entry represents the height of the plant.

def plot_and_show_images(leftimage, rightimage, root):
    for slave in root.pack_slaves():
        slave.pack_forget()
    leftimage_tk = ImageTk.PhotoImage(Image.open(leftimage))
    rightimage_tk = ImageTk.PhotoImage(Image.open(rightimage))

    # Make the new image half the width and half the height of the original image
    #leftimage_resized = leftimage_tk.resize((round(leftimage_tk.size[0] * 0.5),
    #                                         round(leftimage_tk.size[1] * 0.5))
    left_label = tk.Label(root, image=leftimage_tk)
    left_label.image = leftimage_tk
    left_label.pack(side='left')

    right_label = tk.Label(root, image=rightimage_tk)
    right_label.image = rightimage_tk
    right_label.pack(side='left')

    '''
    left_canvas = tk.Canvas(root)
    right_canvas = tk.Canvas(root)
    left_canvas.create_image(20, 20, image=leftimage_tk)
    right_canvas.create_image(0, 0, image=rightimage_tk)
    left_canvas.pack(side="left")
    right_canvas.pack(side="right")
    '''

    # this was for back when we had to draw it in matplotlib and show interactive figure.
    '''
    for fig in figs:
        ax = fig.add_subplot(projection='3d')
        if garden_constants.garden_x_len > garden_constants.garden_y_len:
            ax.pbaspect = [1.0, garden_constants.garden_y_len / garden_constants.garden_x_len,
                           garden_constants.plant_max_radius / garden_constants.garden_x_len]
        else:
            ax.pbaspect = [garden_constants.garden_x_len / garden_constants.garden_y_len, 1.0,
                           garden_constants.plant_max_radius / garden_constants.garden_x_len]

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
        ax.set_xlim(left=-1, right=garden_constants.garden_x_len)
        ax.set_ylim(bottom=-1, top=garden_constants.garden_y_len)
        ax.set_zlim(bottom=0, top=garden_constants.plant_max_radius)
    for _ in range(len(images_to_process)):
        img = images_to_process.pop()
        ax = axes.pop()
        it = np.nditer(img.seed_placement, flags=["multi_index", "refs_ok"])
        for p in it:
            if img.plant_present(p):
                x, y, z, r = img.get_plant_data(it, p)
                color = img.get_plant_color(it)

                # Cylinder
                x_num = 50
                z_num = 2
                rstride = 10
                cstride = 5
                cyl_x = np.linspace(x - r, x + r, x_num)
                cyl_z = np.linspace(0, z, z_num)
                x_grid, z_grid = np.meshgrid(cyl_x, cyl_z, sparse=True)
                y_arc = np.sqrt(np.abs(r ** 2 - (abs(x_grid - x)) ** 2))
                y_grid_1 = y_arc + y
                y_grid_2 = -y_arc + y

                # Draw parameters
                ax.plot_surface(x_grid, y_grid_1, z_grid, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True, antialiased=False)
                ax.plot_surface(x_grid, y_grid_2, z_grid, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True, antialiased=False)

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
                ax.plot_surface(circ_x, circ_y_1, circ_z_1, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
                ax.plot_surface(circ_x, circ_y_2, circ_z_1, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)

                ax.plot_surface(circ_x, circ_y_1, circ_z_2, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
                ax.plot_surface(circ_x, circ_y_2, circ_z_2, alpha=garden_constants.alpha, rstride=rstride,
                                cstride=cstride, color=color, shade=True)
        # Plot the soil
        vertices1 = [[(0,0,0), (garden_constants.garden_x_len, 0,0), (garden_constants.garden_x_len,
                                                               garden_constants.garden_y_len, 0)]]
        poly1 = Poly3DCollection(vertices1, alpha=1, color=garden_constants.soil_color)
        ax.add_collection3d(poly1)
        '''

