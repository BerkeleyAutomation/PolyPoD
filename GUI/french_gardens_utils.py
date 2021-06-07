import plotting_utils
import poisson_disk.poisson_disc as poi
import plotting_utils
import numpy as np
import math


# upper, lower, bounds, num_checks = bmca

corner_width = 2
circle_radius = 3
rectangle_width = 4
corner_length = 6
rectangle_length = 10 - rectangle_width / 2
rectangle_indent = 0
num_checks = 5

def french_demo_bac():
    bounds_map_creator_args = []
    def flip(a):
        return -a + 20

    b_corner1 = [0, corner_length]
    def u_corner1(a):
        if a < corner_width:
            return corner_length
        else:
            return corner_width
    def l_corner1(a):
        return 0

    b_circle1 = [5 - circle_radius, 5 + circle_radius]
    def circle_shift5(a):
        return math.sqrt(math.fabs(circle_radius ** 2 - (a - 5) ** 2))
    def u_circle1(a):
        return circle_shift5(a) + 5
    def l_circle1(a):
        return -circle_shift5(a) + 5

    b_rectl = [rectangle_indent, rectangle_length]
    def u_rectl(a):
        return 10 + rectangle_width / 2
    def l_rectl(a):
        return 10 - rectangle_width / 2

    b_rectd = [10 - rectangle_width / 2, 10 + rectangle_width / 2]
    def u_rectd(a):
        return rectangle_length
    def l_rectd(a):
        return rectangle_indent

    def four_reflections(bn1, un1, ln1, only_horizontal=False, only_vertical=False):
        bn2 = [flip(bn1[1]), flip(bn1[0])]
        def un2(a):
            return un1(flip(a))
        def ln2(a):
            return ln1(flip(a))
        def un3(a):
            return flip(ln1(a))
        def ln3(a):
            return flip(un1(a))
        def un4(a):
            return flip(ln1(flip(a)))
        def ln4(a):
            return flip(un1(flip(a)))

        bounds_map_creator_args.append([un1, ln1, bn1, num_checks])
        if not only_vertical:
            bounds_map_creator_args.append([un2, ln2, bn2, num_checks])
        if not only_horizontal:
            bounds_map_creator_args.append([un3, ln3, bn1, num_checks])
        if not only_vertical and not only_horizontal:
            bounds_map_creator_args.append([un4, ln4, bn2, num_checks])
    four_reflections(b_corner1, u_corner1, l_corner1)
    four_reflections(b_circle1, u_circle1, l_circle1)
    four_reflections(b_rectl, u_rectl, l_rectl, only_horizontal=True)
    four_reflections(b_rectd, u_rectd, l_rectd, only_vertical=True)
    return bounds_map_creator_args
