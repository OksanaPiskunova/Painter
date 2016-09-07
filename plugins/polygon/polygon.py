# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import plugins.base as base


class Polygon(base.Figure):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "polygon"

    @staticmethod
    def get_param_count():
        return base.UNKNOWN_PARAM


class PolygonDrawer(base.Drawer):
    def __init__(self):
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))

    def draw(self, figure):
        self.figure = figure
        point_count = len(figure.points) - 1
        for i in range(point_count):
            self.scene.addLine(figure.points[i][0], figure.points[i][1],
                               figure.points[i + 1][0], figure.points[i + 1][1],
                               self.pen)
        self.scene.addLine(figure.points[0][0], figure.points[0][1],
                           figure.points[point_count][0], figure.points[point_count][1],
                           self.pen)

    def draw_now(self, buffer, curr_point):
        self.scene.removeItem(self.item)
        buffer_len = len(buffer) - 1
        for i in range(buffer_len):
            self.item = QtGui.QGraphicsLineItem(buffer[i][0], buffer[i][1],
                                                buffer[i + 1][0], buffer[i + 1][1])
            self.item.setPen(self.pen)
            self.scene.addItem(self.item)
        self.item = QtGui.QGraphicsLineItem(buffer[buffer_len][0], buffer[buffer_len][1],
                                            curr_point[0], curr_point[1])
        self.item.setPen(self.pen)
        self.scene.addItem(self.item)

    def init_item(self):
        self.item = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.scene.addItem(self.item)

    def set_scene(self, scene):
        self.scene = scene

    def get_scene(self):
        return self.scene

    def set_pen(self, pen):
        self.pen = pen
