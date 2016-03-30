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
        self.pen.setBrush(QtCore.Qt.black)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)

    def draw(self, figure):
        self.figure = figure
        process = self.draw_methods[self.figure.get_type()]
        process()

    def draw_list(self, list):
        for fig in list:
            self.draw(fig)

    def _draw_line(self):
        items = self.scene.items()
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
        self._draw_polygon()

    def _draw_quadrangle(self):
        self._draw_polygon()

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


class CurrentDrawer:
    def __init__(self):
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))
        self.init_item()
        self.pen = QtGui.QPen()
        self._init_pen()

    def _init_pen(self):
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setBrush(QtCore.Qt.black)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)

    def init_item(self):
        self.item = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.scene.addItem(self.item)

    def draw_line(self, buffer, point):
        self.scene.removeItem(self.item)
        self.item = QtGui.QGraphicsLineItem(buffer[0][0], buffer[0][1],
                                            point[0], point[1])
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def draw_polygon(self, buffer, point):
        self.scene.removeItem(self.item)
        buffer_len = len(buffer) - 1
        for i in range(buffer_len):
            self.item = QtGui.QGraphicsLineItem(buffer[i][0], buffer[i][1],
                                                buffer[i + 1][0], buffer[i + 1][1])
            self.item.setPen(self.pen)
            self.scene.addItem(self.item)
        self.item = QtGui.QGraphicsLineItem(buffer[buffer_len][0], buffer[buffer_len][1],
                                            point[0], point[1])
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def draw_triangle(self, buffer, point):
        self.draw_polygon(buffer, point)

    def draw_quadrangle(self, buffer, point):
        self.draw_polygon(buffer, point)

    def draw_rectangle(self, buffer, point):
        self.scene.removeItem(self.item)
        width = figures.Transformation.get_width_of_rect(buffer[0], point)
        height = figures.Transformation.get_height_of_rect(buffer[0], point)
        self.item = QtGui.QGraphicsRectItem(buffer[0][0], buffer[0][1], width, height)
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def draw_square(self, buffer, point):
        self.scene.removeItem(self.item)
        side = figures.Transformation.get_side_of_square(buffer[0], point)
        self.item = QtGui.QGraphicsRectItem(buffer[0][0], buffer[0][1], side, side)
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def draw_ellipse(self, buffer, point):
        self.scene.removeItem(self.item)
        width = figures.Transformation.get_width_of_rect(buffer[0], point)
        height = figures.Transformation.get_height_of_rect(buffer[0], point)
        self.item = QtGui.QGraphicsEllipseItem(buffer[0][0], buffer[0][1], width, height)
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def draw_circle(self, buffer, point):
        self.scene.removeItem(self.item)
        side = figures.Transformation.get_side_of_square(buffer[0], point)
        self.item = QtGui.QGraphicsEllipseItem(buffer[0][0], buffer[0][1], side, side)
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def clear_scene(self):
        self.scene.clear()


class Controller:
    def __init__(self):
        self.drawer = Drawer()
        self.curr_drawer = CurrentDrawer()
        self.list_of_figures = list_of_figures.ListOfFigures()
        self.factory = {"line": figures.Line,
                        "polygon": figures.Polygon,
                        "triangle": figures.Triangle,
                        "quadrangle": figures.Quadrangle,
                        "rectangle": figures.Rectangle,
                        "square": figures.Square,
                        "ellipse": figures.Ellipse,
                        "circle": figures.Circle}
        self.draw_methods = {"line": self.curr_drawer.draw_line,
                             "polygon": self.curr_drawer.draw_polygon,
                             "triangle": self.curr_drawer.draw_triangle,
                             "quadrangle": self.curr_drawer.draw_quadrangle,
                             "rectangle": self.curr_drawer.draw_rectangle,
                             "square": self.curr_drawer.draw_square,
                             "ellipse": self.curr_drawer.draw_ellipse,
                             "circle": self.curr_drawer.draw_circle}
        self.draw_method = None
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
            self._start_drawing()

    def _is_buffer_full(self):
        if self.param_count == len(self.buffer):
            return True
        else:
            return False

    def check_buffer(self):
        if self.param_count == figures.UNKNOWN_PARAM and\
                        len(self.buffer) >= figures.TWO_PARAM:
            self._start_drawing()

    def set_curr_position(self, curr_point):
        if self.buffer != () and self.draw_method != None:
            self.draw_method(self.buffer, curr_point)
            self.scene = self.curr_drawer.scene

    def _start_drawing(self):
        self._init_const_scene()
        self._process_figure()
        self._init_buffer()
        self.scene = self.drawer.scene
        self.figure_type = None
        self.draw_method = None

    def _init_new_scene(self):
        self.curr_drawer.clear_scene()
        items = self.drawer.scene.items()
        for item in items:
            self.curr_drawer.scene.addItem(item)

    def _init_const_scene(self):
        self._remote_items()
        items = self.curr_drawer.scene.items()
        for item in items:
            self.drawer.scene.addItem(item)
        self.curr_drawer.clear_scene()

    def _remote_items(self):
        self.curr_drawer.scene.removeItem(self.curr_drawer.item)

    def _prepare_to_draw(self):
        self._init_new_scene()
        self.curr_drawer.init_item()
        self.scene = self.curr_drawer.scene

    def process_list(self):
        self.drawer.draw_list(list_of_figures.fig_list.list)
        self.scene = self.drawer.scene

    def process_line(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Line.get_type()
        self.param_count = figures.Line.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_polygon(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Polygon.get_type()
        self.param_count = figures.Polygon.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_triangle(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Triangle.get_type()
        self.param_count = figures.Triangle.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_quadrangle(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Quadrangle.get_type()
        self.param_count = figures.Quadrangle.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_rectangle(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Rectangle.get_type()
        self.param_count = figures.Rectangle.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_square(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Square.get_type()
        self.param_count = figures.Square.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_ellipse(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Ellipse.get_type()
        self.param_count = figures.Ellipse.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def process_circle(self):
        self._init_buffer()
        self._prepare_to_draw()
        self.figure_type = figures.Circle.get_type()
        self.param_count = figures.Circle.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]

    def _process_figure(self):
        self.create_figure()
        self._draw_figure()

    def create_figure(self):
        fig = self.factory[self.figure_type]
        self.figure = fig(self.buffer)
        self.list_of_figures.add_figure(self.figure)

    def _draw_figure(self):
        self.drawer.draw(self.figure)
        self.scene = self.drawer.scene

    def set_pen(self, pen):
        self.drawer.pen = pen
        self.curr_drawer.pen = pen

    def clear_scene(self):
        self.drawer.clear_scene()
