# module contains classes of figures


class Figure:
    """abstract class"""
    pass

    @staticmethod
    def get_type():
        pass

    @staticmethod
    def get_param_count():
        pass


class Line(Figure):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "line"

    @staticmethod
    def get_param_count():
        return TWO_PARAM


class Polygon(Figure):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "polygon"

    @staticmethod
    def get_param_count():
        return UNKNOWN_PARAM


class Triangle(Polygon):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "triangle"

    @staticmethod
    def get_param_count():
        return THREE_PARAM


class Quadrangle(Polygon):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "quadrangle"

    @staticmethod
    def get_param_count():
        return FOUR_PARAM


class Rectangle(Quadrangle):
    def __init__(self, points):
        self.points = points
        self.width = Transformation.get_width_of_rect(self.points[0], self.points[1])
        self.height = Transformation.get_height_of_rect(self.points[0], self.points[1])

    @staticmethod
    def get_type():
        return "rectangle"

    @staticmethod
    def get_param_count():
        return TWO_PARAM


class Square(Rectangle):
    def __init__(self, points):
        point_a = points[0]
        point_b = points[1]
        self.side = Transformation.get_side_of_square(point_a, point_b)
        self.points = Transformation.get_new_coord_square(point_a, point_b, self.side)

    @staticmethod
    def get_type():
        return "square"

    @staticmethod
    def get_param_count():
        return TWO_PARAM


class Ellipse(Figure):
    def __init__(self, points):
        self.points = points
        self.width = Transformation.get_width_of_rect(self.points[0], self.points[1])
        self.height = Transformation.get_height_of_rect(self.points[0], self.points[1])
        self.center = Transformation.get_center_of_rect(self.points[0], self.points[1])

    @staticmethod
    def get_type():
        return "ellipse"

    @staticmethod
    def get_param_count():
        return TWO_PARAM


class Circle(Ellipse):
    def __init__(self, points):
        self.points = points
        self.side = Transformation.get_side_of_square(self.points[0], self.points[1])
        self.points = Transformation.get_new_coord_square(self.points[0], self.points[1], self.side)
        self.center = Transformation.get_center_of_rect(self.points[0], self.points[1])

    @staticmethod
    def get_type():
        return "circle"

    @staticmethod
    def get_param_count():
        return TWO_PARAM


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


UNKNOWN_PARAM = 0
ONE_PARAM = 1
TWO_PARAM = 2
THREE_PARAM = 3
FOUR_PARAM = 4
