# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import plugins.base as base


class Line(base.Figure):
    def __init__(self, points):
        self.points = points

    @staticmethod
    def get_type():
        return "line"

    @staticmethod
    def get_param_count():
        return base.TWO_PARAM


class LineDrawer(base.Drawer):
    def __init__(self):
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))

    def draw(self, figure):
        self.figure = figure
        self.scene.addLine(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.points[1][0], self.figure.points[1][1],
                           self.pen)

    def draw_now(self, buffer, curr_point):
        self.scene.removeItem(self.item)
        self.item = QtGui.QGraphicsLineItem(buffer[0][0], buffer[0][1],
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
