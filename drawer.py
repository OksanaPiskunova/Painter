# universal drawer

import figures, list_of_figures
from PyQt4 import QtGui, QtCore


class Drawer:
    def __init__(self):
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))
        self.draw_methods = {"line": self._draw_line,
                             "polygon": self._draw_polygon,
                             "triangle": self._draw_triangle,
                             "quadrangle": self._draw_quadrangle,
                             "rectangle": self._draw_rectangle,
                             "square": self._draw_square,
                             "ellipse": self._draw_ellipse,
                             "circle": self._draw_circle}
        self.pen = QtGui.QPen()
        self._init_pen()

    def _init_pen(self):
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setBrush(QtCore.Qt.red)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)

    def draw(self, figure):
        self.figure = figure
        process = self.draw_methods[self.figure.get_type()]
        process()

    def draw_list(self):
        for fig in list_of_figures.fig_list.list:
            self.draw(fig)

    def _draw_line(self):
        self.scene.addLine(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.points[1][0], self.figure.points[1][1], self.pen)

    def _draw_polygon(self):
        point_count = len(self.figure.points) - 1
        for i in range(point_count):
            self.scene.addLine(self.figure.points[i][0], self.figure.points[i][1],
                               self.figure.points[i + 1][0], self.figure.points[i + 1][1],
                               self.pen)
        self.scene.addLine(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.points[point_count][0], self.figure.points[point_count][1],
                           self.pen)

    def _draw_triangle(self):
        self.scene.addLine(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.points[1][0], self.figure.points[1][1], self.pen)
        self.scene.addLine(self.figure.points[1][0], self.figure.points[1][1],
                           self.figure.points[2][0], self.figure.points[2][1], self.pen)
        self.scene.addLine(self.figure.points[2][0], self.figure.points[2][1],
                           self.figure.points[0][0], self.figure.points[0][1], self.pen)

    def _draw_quadrangle(self):
        self.scene.addLine(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.points[1][0], self.figure.points[1][1], self.pen)
        self.scene.addLine(self.figure.points[1][0], self.figure.points[1][1],
                           self.figure.points[2][0], self.figure.points[2][1], self.pen)
        self.scene.addLine(self.figure.points[2][0], self.figure.points[2][1],
                           self.figure.points[3][0], self.figure.points[3][1], self.pen)
        self.scene.addLine(self.figure.points[3][0], self.figure.points[3][1],
                           self.figure.points[0][0], self.figure.points[0][1], self.pen)

    def _draw_rectangle(self):
        self.scene.addRect(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.width, self.figure.height, self.pen)

    def _draw_square(self):
        self.scene.addRect(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.side, self.figure.side, self.pen)

    def _draw_ellipse(self):
        self.scene.addEllipse(self.figure.points[0][0], self.figure.points[0][1],
                              self.figure.width, self.figure.height, self.pen)

    def _draw_circle(self):
        self.scene.addEllipse(self.figure.points[0][0], self.figure.points[0][1],
                              self.figure.side, self.figure.side, self.pen)

    def clear_scene(self):
        self.scene.clear()


class Controller:
    def __init__(self):
        self.factory = {"line": figures.Line,
                        "polygon": figures.Polygon,
                        "triangle": figures.Triangle,
                        "quadrangle": figures.Quadrangle,
                        "rectangle": figures.Rectangle,
                        "square": figures.Square,
                        "ellipse": figures.Ellipse,
                        "circle": figures.Circle}
        self.drawer = Drawer()
        self.scene = None
        self.figure = None
        self.figure_type = ""
        self._init_buffer()
        self.param_count = 0

    def _init_buffer(self):
        self.buffer = ()

    def add_to_buffer(self, point):
        self.buffer += point,
        if self._is_buffer_full():
            self._process_figure()

    def _is_buffer_full(self):
        if self.param_count == len(self.buffer):
            return True
        else:
            return False

    def check_buffer(self):
        if self.param_count == figures.unknown_param and len(self.buffer) >= figures.two_param:
            self._process_figure()

    def process_list(self):
        self.drawer.draw_list()
        self.scene = self.drawer.scene

    def process_line(self):
        self._init_buffer()
        self.figure_type = figures.Line.get_type()
        self.param_count = figures.Line.get_param_count()

    def process_polygon(self):
        self._init_buffer()
        self.figure_type = figures.Polygon.get_type()
        self.param_count = figures.Polygon.get_param_count()

    def process_triangle(self):
        self._init_buffer()
        self.figure_type = figures.Triangle.get_type()
        self.param_count = figures.Triangle.get_param_count()

    def process_quadrangle(self):
        self._init_buffer()
        self.figure_type = figures.Quadrangle.get_type()
        self.param_count = figures.Quadrangle.get_param_count()

    def process_rectangle(self):
        self._init_buffer()
        self.figure_type = figures.Rectangle.get_type()
        self.param_count = figures.Rectangle.get_param_count()

    def process_square(self):
        self._init_buffer()
        self.figure_type = figures.Square.get_type()
        self.param_count = figures.Square.get_param_count()

    def process_ellipse(self):
        self._init_buffer()
        self.figure_type = figures.Ellipse.get_type()
        self.param_count = figures.Ellipse.get_param_count()

    def process_circle(self):
        self._init_buffer()
        self.figure_type = figures.Circle.get_type()
        self.param_count = figures.Circle.get_param_count()

    def _process_figure(self):
        self.create_figure()
        self._draw_figure()

    def create_figure(self):
        fig = self.factory[self.figure_type]
        self.figure = fig(self.buffer)

    def _draw_figure(self):
        self.drawer.draw(self.figure)
        self.scene = self.drawer.scene

    def clear_scene(self):
        self.drawer.clear_scene()
