# universal drawer

from PyQt4 import QtGui, QtCore
import plugins.base as base


class Drawer:
    def __init__(self):
        self.scene = None
        self.draw_methods = {}
        self.pen = QtGui.QPen()
        self._init_pen()

    def init_item(self):
        self.item = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.scene.addItem(self.item)

    def _init_pen(self):
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setBrush(QtCore.Qt.black)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)

    def draw(self, figure):
        self.figure = figure
        process = self.draw_methods[self.figure.get_type()]
        process(self.figure)

    def set_scene(self, scene):
        self.scene = scene

    def clear_scene(self):
        self.scene.clear()


class Controller:
    def __init__(self):
        self.drawer = Drawer()
        self.list_of_figures = []
        self.factory = {}
        self.draw_methods = {}
        self.draw_method = None
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))
        self.figure = None
        self.figure_type = ""
        self.init_buffer()
        self.param_count = 0
        self.is_figure_chosen = False

    def init_buffer(self):
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

    def check_buffer(self, curr_point):
        if self.param_count == base.UNKNOWN_PARAM and\
                        len(self.buffer) >= base.TWO_PARAM:
            self.buffer += curr_point,
            self._start_drawing()

    def set_curr_position(self, curr_point):
        if self.buffer != () and self.draw_method != None:
            self.draw_method(self.buffer, curr_point)

    def _start_drawing(self):
        self._process_figure()
        self.init_buffer()
        self.scene = self.drawer.scene
        self.figure_type = None
        self.draw_method = None

    def prepare_to_draw(self):
        self.drawer.set_scene(self.scene)
        self.drawer.init_item()

    def process_plugin_figure(self, figure, drawer):
        self.init_buffer()
        self.prepare_to_draw()
        self.figure_type = figure.get_type()
        self.param_count = figure.get_param_count()
        self.draw_method = self.draw_methods[self.figure_type]
        self.plugin_drawer = drawer

    def _process_figure(self):
        self.create_figure()
        self._draw_figures()

    def create_figure(self):
        fig = self.factory[self.figure_type]
        self.figure = fig(self.buffer)
        self.list_of_figures.append(self.figure)

    def _draw_figures(self):
        self.plugin_drawer.set_scene(self.scene)
        self.drawer.draw(self.figure)
        self.is_figure_chosen = False

    def set_pen(self, pen):
        self.drawer.pen = pen

    def clear_scene(self):
        self.drawer.clear_scene()
