# this module contains class with the list of different figures

import figures


class StaticListOfFigures:
    def __init__(self):
        self.list = []
        self._create_figures()

    def add(self, object):
        self.list.append(object)

    def _create_figures(self):
        self.list.append(figures.Line(((0, 0), (1, 1))))
        self.list.append(figures.Polygon(((200, 100), (300, 200), (300, 300), (100, 300), (100, 200))))
        self.list.append(figures.Triangle(((18, 65), (56, 87), (74, 23))))
        self.list.append(figures.Quadrangle(((96, 111), (120, 120), (84, 36), (133, 133))))
        self.list.append(figures.Rectangle(((156, 156), (170, 180))))
        self.list.append(figures.Square(((156, 156), (170, 180))))
        self.list.append(figures.Ellipse(((20, 156), (50, 180))))
        #self.list.append(figures.Ellipse(((10, 200), (60, 400))))
        self.list.append(figures.Circle(((10, 200), (60, 400))))


class ListOfFigures:
    def __init__(self):
        self._init_list()

    def _init_list(self):
        self.list = []

    def add_figure(self, figure):
        self.list.append(figure)

    def get_element_count(self):
        return len(self.list)

    def delete_figure(self, figure):
        self.list.remove(figure)


fig_list = StaticListOfFigures()
