import plotting_utils
import poisson_disk.poisson_disc as poi
import plotting_utils
import numpy as np
import math

beta = 1
num_p_selector = poi.weighted_round_or_one
fill_final = False
data = False
bounds_map_creator_args = None
save_plotly=False
show=True
save=True

# upper, lower, bounds, num_checks = bmca
corner_length = 5
corner_width = 2
circle_radius = 2
rectangle_width = 3
rectangle_length = 8.5
num_checks = 5

def french_demo_bmc():
    bounds_map_creator_args = []
    for x in range(2):
        for y in range(2):
            bounds_corner = [15 * x, 15 * x + corner_length]
            bounds_circle = [5 - circle_radius, 5 + circle_radius]
            if x == 0:
                bounds_rectangle = [10 - rectangle_width / 2, 10 + rectangle_width / 2]
            else:
                bounds_rectangle = [0 + y * (20 - rectangle_length),
                                    rectangle_length + y * (20 - rectangle_length)]

            if x == 0:
                def upper_corner(a):
                    return 100
                    if a < corner_width or a > (20 - corner_width):
                        return corner_length
                    else:
                        return corner_width
                def lower_corner(a):
                    return 0
            else:
                def lower_corner(a):
                    if a < corner_width or a > (20 - corner_width):
                        return 20 - corner_length
                    else:
                        return 20 - corner_width
                def upper_corner(a):
                    return 20
            def upper_circle_helper(a):
                return math.sqrt(math.fabs(circle_radius ** 2 - a ** 2))
            def lower_circle_helper(a):
                return -upper_circle(a)
            def upper_circle(a):
                return upper_circle_helper(5 + 10 * x) + 5 + 10 * y
            def lower_circle(a):
                return lower_circle_helper(5 + 10 * a) + 5 + 10 * y

            if x == 0:
                def lower_rectangle(a):
                    return 0 + (20 - rectangle_length) * y
                def upper_rectangle(a):
                    return lower_rectangle(a) + rectangle_length
            else:
                def lower_rectangle(a):
                    return 10 - rectangle_width / 2
                def upper_rectangle(a):
                    return lower_rectangle(a) + rectangle_width
            bounds_map_creator_args.append([upper_corner, lower_corner, bounds_corner, num_checks])
            #bounds_map_creator_args.append([upper_circle, lower_circle, bounds_circle, num_checks])
            #bounds_map_creator_args.append([upper_rectangle, lower_rectangle, bounds_rectangle, num_checks])
    return bounds_map_creator_args
bounds_map_creator_args = french_demo_bmc()
if False:
    plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                    data=data, save_plotly=save_plotly, show=show, save=save)