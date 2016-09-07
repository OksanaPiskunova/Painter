# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import plugins.base as base
from plugins.transformation import Transformation


class Rectangle(base.Figure):
    def __init__(self, points):
        self.points = points
        self.width = Transformation.get_width_of_rect(self.points[0], self.points[1])
        self.height = Transformation.get_height_of_rect(self.points[0], self.points[1])

    @staticmethod
    def get_type():
        return "rectangle"

    @staticmethod
    def get_param_count():
        return base.TWO_PARAM


class RectangleDrawer(base.Drawer):
    def __init__(self):
        self.scene = QtGui.QGraphicsScene(QtCore.QRectF(0, 0, 678, 538))

    def draw(self, figure):
        self.figure = figure
        self.scene.addRect(self.figure.points[0][0], self.figure.points[0][1],
                           self.figure.width, self.figure.height, self.pen)

    def draw_now(self, buffer, curr_point):
        self.scene.removeItem(self.item)
        width = Transformation.get_width_of_rect(buffer[0], curr_point)
        height = Transformation.get_height_of_rect(buffer[0], curr_point)
        self.item = QtGui.QGraphicsRectItem(buffer[0][0], buffer[0][1], width, height)
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
