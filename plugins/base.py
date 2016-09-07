# -*- coding: utf-8 -*-


class Figure:
    def __init__(self):
        pass

    @staticmethod
    def get_type():
        pass

    @staticmethod
    def get_param_count():
        pass


class Drawer:
    def draw(self, figure):
        pass

    def draw_now(self, buffer, curr_point):
        pass

    def init_item(self):
        pass

    def set_scene(self, scene):
        pass

    def get_scene(self):
        pass

    def set_pen(self, pen):
        pass


UNKNOWN_PARAM = 0
ONE_PARAM = 1
TWO_PARAM = 2
THREE_PARAM = 3
FOUR_PARAM = 4
