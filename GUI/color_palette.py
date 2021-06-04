import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import garden_constants
from datetime import datetime

fig, ax = plt.subplots()
color_dicts = [garden_constants.colors_of_plants_hcl_v2]

def color_palette(color_dict):
    y_len = (len(color_dict) - 1) // 3 + 1
    for count, color in enumerate(color_dict):
        x = count % 3
        y = y_len - 1 - count // 3
        ax.add_patch(Rectangle((x, y), 1, 1, color=color))
        ax.text(x, y + 0.5, color)
        ax.text(x + 0.8, y + 0.5, count)

    plt.xlim(0, 3)
    plt.ylim(0, y_len)
    fig_filename = "color_palette_{0}".format(datetime.now().strftime("%m-%d-%y_%H-%M-%S-%f"))
    plt.savefig(fig_filename, dpi=200)

def main():
    for color_dict in color_dicts:
        color_palette(color_dict)

main()