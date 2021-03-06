# -*- coding: utf-8 -*-


class Transformation:
    def __init__(self):
        pass

    @staticmethod
    def get_width_of_rect(point_a, point_b):
        return abs(point_b[0] - point_a[0])

    @staticmethod
    def get_height_of_rect(point_a, point_b):
        return abs(point_b[1] - point_a[1])

    @staticmethod
    def get_center_of_rect(point_a, point_b):
        width = Transformation.get_width_of_rect(point_a, point_b)
        height = Transformation.get_height_of_rect(point_a, point_b)
        if point_a[0] < point_b[0]:
            center_x = point_a[0] + width / 2
        else:
            center_x = point_a[0] - width / 2
        if point_a[1] < point_b[1]:
            center_y = point_a[1] + height / 2
        else:
            center_y = point_a[1] - height / 2
        return center_x, center_y

    @staticmethod
    def get_side_of_square(point_a, point_b):
        return min(abs(point_a[0] - point_b[0]),
                   abs(point_a[1] - point_b[1]))

    @staticmethod
    def get_new_coord_square(point_a, point_b, side):
        return point_a, (Transformation._get_new_x_square(point_a, point_b, side),
                         Transformation._get_new_y_square(point_a, point_b, side))

    @staticmethod
    def _get_new_x_square(point_a, point_b, side):
        if point_a[0] < point_b[0]:
            return point_a[0] + side
        else:
            return point_a[0] - side

    @staticmethod
    def _get_new_y_square(point_a, point_b, side):
        if point_a[1] < point_b[1]:
            return point_a[1] + side
        else:
            return point_a[1] - side